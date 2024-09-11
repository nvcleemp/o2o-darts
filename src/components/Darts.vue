<template>
  <div class="graph">
    <div ref="drawing"></div>
  </div>
  <div class="names">
    {{ participantCount }}
    <Slider
      id="participantCount"
      v-model="participantCount"
      :min="27"
      :max="30"
      style="width: 25rem; margin-top: 10px"
    />
    <div
      v-for="participant in participants"
      :key="participant.index"
      class="name"
      :class="{ hidden: participant.index >= participantCount }"
    >
      <label :for="'participant' + participant.index">{{ participant.index + 1 }}</label>
      <InputText :id="'participant' + participant.index" v-model="participant.name" @update:model-value="currentParticipant = participant.index" /> vs.
      <span class="opponent" v-for="opp in [0,1,2,3]" :key="opp">
        {{ opponent(participant.index, opp) }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

import * as d3 from 'd3'

import InputText from 'primevue/inputtext'
import Slider from 'primevue/slider'

const participantCount = ref(27)

const currentParticipant = ref(-1)

class Participant {
  name: string
  index: number
  constructor(name: string, index: number) {
    this.name = name
    this.index = index
  }
}

const participantsArray = Array(40) as Participant[]

for (let i = 0; i < participantsArray.length; i++) {
  const name = localStorage.getItem('participant' + i) || ''
  participantsArray[i] = new Participant(name, i)
}

const participants = ref(participantsArray)

watch(
  participants,
  (newParticipants) => {
    for (let i = 0; i < newParticipants.length; i++) {
      localStorage.setItem('participant' + i, newParticipants[i].name)
    }
  },
  { deep: true }
)

//Graph

class Vertex {
  index: number
  x: number
  y: number
  constructor(index: number, x: number, y: number) {
    this.index = index
    this.x = x
    this.y = y
  }
}

class Graph {
  vertices: Vertex[]
  edges: Map<Vertex, Vertex[]>
  constructor(vertices: Vertex[], edges: Map<Vertex, Vertex[]>) {
    this.vertices = vertices
    this.edges = edges
  }
}

const drawing = ref<HTMLDivElement | null>(null);
const graph = ref<Graph | null>(null);
let edgesGroup: d3.Selection<SVGGElement, unknown, null, undefined>;
let verticesGroup: d3.Selection<SVGGElement, unknown, null, undefined>;

let x: d3.ScaleTime<number, number, never>
let y: d3.ScaleLinear<number, number, never>
let line: d3.Line<{ date: Date; value: number }>

const vs = [new Vertex(0, 0, 0), new Vertex(1, 0, 1), new Vertex(2, 1, 0), new Vertex(3, 1, 1)]
const es = new Map<Vertex, Vertex[]>()
es.set(vs[0], [vs[1], vs[2]])
es.set(vs[1], [vs[0], vs[2]])
es.set(vs[2], [vs[0], vs[1]])
graph.value = new Graph(vs, es);

const constructGraph = (order: number, input: any) => {
    const vertices = Array(order).fill(0).map((_, i) => new Vertex(i, input[i][0][0], input[i][0][1]));
    const edges = new Map<Vertex, Vertex[]>();
    for (let i = 0; i < order; i++) {
        edges.set(vertices[i], vertices.filter((_, j) => input[i][1].includes(j)));
    }
    return new Graph(vertices, edges);
}

const graphs: any = {
    27: constructGraph(27, {
        0:[[0.20471390453002636, -1.1827692711967828],[1, 2, 3, 4]],
        1:[[1.1590921960427805, 0.09947649114407908],[0, 19, 21, 26]],
        2:[[0.5672769780440112, -0.9742678039541879],[0, 20, 22, 25]],
        3:[[-0.11102142919816316, -1.2000000000000002],[0, 15, 18, 23]],
        4:[[-0.7244082604105304, -0.8106924589905251],[0, 16, 17, 24]],
        5:[[-1.0180794159877111, -0.3916535090892963],[6, 7, 23, 24]],
        6:[[0.9805722201837495, 0.6671739722273425],[5, 13, 18, 26]],
        7:[[-0.42184549546347394, -0.14460593591464121],[5, 14, 17, 25]],
        8:[[-1.082393853671336, 0.5942800654565251],[11, 12, 15, 16]],
        9:[[-0.6331282273862615, 0.6233470525218702],[11, 13, 23, 25]],
        10:[[-0.062081453536551034, 1.1685870590716227],[12, 14, 24, 26]],
        11:[[-0.76790578836273, 0.9013646327727289],[8, 9, 14, 20]],
        12:[[0.22588798440815916, 1.2000000000000002],[8, 10, 13, 19]],
        13:[[0.5451561915522518, 1.0544574234490156],[6, 9, 12, 21]],
        14:[[-0.4196979880137093, 1.0263045850368355],[7, 10, 11, 22]],
        15:[[-0.41622433884619703, -1.1352629744173939],[3, 8, 22, 24]],
        16:[[-1.1927266433562977, 0.1682283143476787],[4, 8, 21, 23]],
        17:[[-0.07440355283908939, -0.12557674314921874],[4, 7, 20, 26]],
        18:[[1.0307321053435063, -0.4445392963207324],[3, 6, 19, 25]],
        19:[[1.198221769831778, -0.25412921509156594],[1, 12, 18, 22]],
        20:[[0.16556157828365636, 0.2415381436792885],[2, 11, 17, 21]],
        21:[[0.4688519935051063, 0.6318900276202459],[1, 13, 16, 20]],
        22:[[0.7895214523232092, -0.9069756724940188],[2, 14, 15, 19]],
        23:[[-1.1982217698317779, -0.12751315545642727],[3, 5, 9, 16]],
        24:[[-0.9138961900299885, -0.8094034130971139],[4, 5, 10, 15]],
        25:[[0.4693560653476747, -0.5326423658473995],[2, 7, 9, 18]],
        26:[[1.0397111244519506, 0.5033001785553033],[1, 6, 10, 17]],
    }),
    28: constructGraph(28, {
        0:[[1.1013511392623014, 0.5301404681929371],[1, 2, 3, 4]],
        1:[[0.8690990159203703, 0.8218737626820332],[0, 18, 19, 27]],
        2:[[0.5708317029204304, 0.5666774106195679],[0, 20, 21, 27]],
        3:[[1.0265752506510855, 0.2281539200504501],[0, 22, 24, 26]],
        4:[[1.2000000000000002, -0.1738092795847228],[0, 23, 25, 26]],
        5:[[0.24064814338013907, -0.908939879659031],[6, 7, 8, 9]],
        6:[[0.49854046407598296, -0.1904750154353021],[5, 18, 19, 26]],
        7:[[0.6949139804626419, -0.9412077556399218],[5, 23, 25, 27]],
        8:[[-0.03895460134791884, -1.1245937894762443],[5, 22, 24, 27]],
        9:[[0.0016884353648856099, -0.43093414405242214],[5, 20, 21, 26]],
        10:[[-0.920748245842453, -0.6101837521409963],[14, 17, 18, 21]],
        11:[[-1.2000000000000002, 0.04960672010896772],[15, 16, 18, 21]],
        12:[[0.055675632820586296, 1.0948140275025926],[14, 17, 19, 20]],
        13:[[-0.5612878343884331, 1.1019248797783332],[15, 16, 19, 20]],
        14:[[-0.6073127879621322, -0.9751260007653002],[10, 12, 22, 23]],
        15:[[-1.080213046475345, 0.07118660644504227],[11, 13, 22, 23]],
        16:[[-0.9293423137787294, 0.7312002948695427],[11, 13, 24, 25]],
        17:[[-0.4030466955674451, 0.5754286365617656],[10, 12, 24, 25]],
        18:[[-0.6248185188527615, -0.22048231802478657],[1, 6, 10, 11]],
        19:[[0.4212724089936355, 1.1090268077099796],[1, 6, 12, 13]],
        20:[[-0.09650234120418122, 1.1245937894762443],[2, 9, 12, 13]],
        21:[[-1.0245373930707062, -0.41873147509977837],[2, 9, 10, 11]],
        22:[[-0.4216722468644757, -1.066372933357692],[3, 8, 14, 15]],
        23:[[0.5179484680142399, -1.0962259002697317],[4, 7, 14, 15]],
        24:[[-0.68458802697254, 0.5771757010156819],[3, 8, 16, 17]],
        25:[[-0.023993786425555275, 0.29426580550823933],[4, 7, 16, 17]],
        26:[[1.024933509823967, -0.1489322313522281],[3, 4, 6, 9]],
        27:[[0.9222771397425746, -0.6733140165159646],[1, 2, 7, 8]],
    }),
    29: constructGraph(29, {
        0:[[4.440892098500626e-16, 1.1982400966213491],[1, 2, 3, 4]],
        1:[[-0.25834341112163284, 1.1701435574783141],[0, 22, 25, 27]],
        2:[[-0.6195732862121988, -1.0332612036779762],[0, 21, 25, 26]],
        3:[[0.2583434111216336, 1.1701435574783141],[0, 23, 26, 28]],
        4:[[0.6195732862121988, -1.0332612036779762],[0, 24, 27, 28]],
        5:[[-1.1859310971704629, -0.19794592632447494],[6, 7, 13, 20]],
        6:[[1.1164093743049817, -0.4483405421443698],[5, 8, 14, 18]],
        7:[[-1.1164093743049808, -0.4483405421443707],[5, 8, 16, 17]],
        8:[[1.1859310971704633, -0.19794592632447516],[6, 7, 15, 19]],
        9:[[-0.12993338060500192, -1.1982400966213493],[10, 17, 22, 25]],
        10:[[0.12993338060500337, -1.1982400966213493],[9, 18, 23, 28]],
        11:[[1.1579582365337449, 0.31798313018198165],[12, 19, 21, 26]],
        12:[[-1.1579582365337453, 0.31798313018198066],[11, 20, 24, 27]],
        13:[[0.9159377677966476, 0.7744821608404492],[5, 17, 21, 25]],
        14:[[0.9946855898968981, -0.6779359556245872],[6, 20, 22, 27]],
        15:[[-0.9159377677966462, 0.7744821608404502],[8, 18, 24, 28]],
        16:[[-0.9946855898968971, -0.6779359556245885],[7, 19, 23, 26]],
        17:[[0.7272756706575194, 0.9531923918985609],[7, 9, 13, 23]],
        18:[[-0.727275670657519, 0.9531923918985613],[6, 10, 15, 22]],
        19:[[1.2000000000000002, 0.06153971789298496],[8, 11, 16, 24]],
        20:[[-1.2000000000000002, 0.0615397178929844],[5, 12, 14, 21]],
        21:[[1.061771632905316, 0.5593933016002657],[2, 11, 13, 20]],
        22:[[-0.504606971467298, 1.0871677029924784],[1, 9, 14, 18]],
        23:[[0.504606971467298, 1.087167702992479],[3, 10, 16, 17]],
        24:[[-1.061771632905316, 0.5593933016002652],[4, 12, 15, 19]],
        25:[[-0.38372460134849595, -1.1423764245678214],[1, 2, 9, 13]],
        26:[[-0.8264514128188667, -0.8759965404077672],[2, 3, 11, 16]],
        27:[[0.8264514128188676, -0.8759965404077663],[1, 4, 12, 14]],
        28:[[0.38372460134849673, -1.1423764245678214],[3, 4, 10, 15]],
    }),
    30: constructGraph(30, {
        0:[[0.6917933463978461, 0.6055192071423336],[1, 2, 3, 4]],
        1:[[0.3811825085133367, 0.8323996037475716],[0, 25, 26, 29]],
        2:[[0.49757774640737207, 1.0866144947401053],[0, 25, 26, 29]],
        3:[[0.8837986319669922, 0.26952505722088127],[0, 27, 28, 29]],
        4:[[1.1500956499704396, 0.35396084907011305],[0, 27, 28, 29]],
        5:[[-1.0468045096999261, -0.6118324393329715],[7, 8, 9, 10]],
        6:[[-0.8054439639785829, -0.4718825150308712],[7, 8, 9, 10]],
        7:[[-0.7126593039042612, -0.9859912726031547],[5, 6, 11, 12]],
        8:[[-0.5484882945685767, -0.7598857813305385],[5, 6, 11, 12]],
        9:[[-1.2000000000000002, -0.13357027426491452],[5, 6, 13, 14]],
        10:[[-0.9226835593631276, -0.10500129054520113],[5, 6, 13, 14]],
        11:[[-0.25499677565059653, -1.1918403561672362],[7, 8, 15, 16]],
        12:[[-0.19726710891534294, -0.9188025889812605],[7, 8, 15, 16]],
        13:[[-1.145148233954043, 0.3663653833644168],[9, 10, 17, 18]],
        14:[[-0.8808541184998107, 0.27773527916753693],[9, 10, 17, 18]],
        15:[[0.2454478301191403, -1.193887215710732],[11, 12, 19, 20]],
        16:[[0.18925292727020637, -0.9201688593001967],[11, 12, 19, 20]],
        17:[[-0.686753092091152, 0.6105934617289908],[13, 14, 21, 22]],
        18:[[-0.8908094081957151, 0.8006345142217887],[13, 14, 21, 22]],
        19:[[0.7042072800960124, -0.9924668572562839],[15, 16, 23, 24]],
        20:[[0.5423674911777869, -0.7653709467167151],[15, 16, 23, 24]],
        21:[[-0.37374866167675225, 0.8360130537564209],[17, 18, 25, 26]],
        22:[[-0.48256400719802384, 1.0927822655993573],[17, 18, 25, 26]],
        23:[[1.0414661775153697, -0.622694424937213],[19, 20, 27, 28]],
        24:[[0.8021170565211313, -0.4792269271156795],[19, 20, 27, 28]],
        25:[[0.004043001688830206, 0.9147779404690799],[1, 2, 21, 22]],
        26:[[0.00820705887131501, 1.1938872157107325],[1, 2, 21, 22]],
        27:[[0.9226607313689127, -0.11381849091173857],[3, 4, 23, 24]],
        28:[[1.2000000000000002, -0.14529390773275752],[3, 4, 23, 24]],
        29:[[0.9026817378074594, 0.7885968260443307],[1, 2, 3, 4]],
    })
}

graph.value = graphs[27];

watch(participantCount, (newCount: number) => {
    graph.value = graphs[newCount] as Graph;
});

const setupGraph = () => {
    if (!drawing.value) return

    const margin = { top: 20, right: 30, bottom: 30, left: 40 }
    const width = drawing.value.clientWidth / 2 - margin.left - margin.right
    const height = drawing.value.clientHeight - margin.top - margin.bottom

    const svg = d3
        .select(drawing.value)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);
    
    edgesGroup = svg
        .append("g")
        .classed("edges", true)
        .attr("fill", "none")
        .attr("stroke-width", 1.5)
        .attr("stroke", "currentColor");
    verticesGroup = svg
        .append("g")
        .classed("vertices", true)
        .attr("fill", "currentColor")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round");
}

const updateGraph = () => {
  if (!drawing.value) return
  if (!graph.value) return

  const { vertices, edges } = graph.value

  const edgeList = [];
  for (const [from, tos] of edges) {
    for (const to of tos) {
        if(to.index < from.index) continue;
        edgeList.push({ source: from, target: to});
    }
  }

    const minX = Math.min(...vertices.map((v) => v.x));
    const maxX = Math.max(...vertices.map((v) => v.x));
    const minY = Math.min(...vertices.map((v) => v.y));
    const maxY = Math.max(...vertices.map((v) => v.y));

    const margin = { top: 20, right: 30, bottom: 30, left: 40 }
    const width = drawing.value.clientWidth / 2 - margin.left - margin.right
    const height = drawing.value.clientHeight - margin.top - margin.bottom

    const size = Math.min(width, height);

    const y = d3.scaleLinear().nice().domain([minY, maxY]).range([size, 0]);
    const x = d3.scaleLinear().nice().domain([minX, maxX]).range([0, size]);

  edgesGroup
    .selectAll("path")
    .data(edgeList)
    .join(
        enter => enter.append("path").attr("d", "M0,0 L0,0"),
        update => update,
        exit => exit.remove()
    )
    .transition()
    .duration(1000)
    .attr("d", (d) => `M${x(d.source.x)},${y(d.source.y)} L${x(d.target.x)},${y(d.target.y)}`)
    .attr("stroke", (d) => (currentParticipant.value == d.source.index || currentParticipant.value == d.target.index) ? "blue" : "currentColor")
    .attr("stroke-width", (d) => (currentParticipant.value == d.source.index || currentParticipant.value == d.target.index) ? 3 : 1.5);
  

  verticesGroup
    .selectAll('g')
    .data(vertices)
    .join('g')
    .call(el => {
        el.selectAll('circle').remove();
        el.append('circle').attr('r', 4).attr('stroke', 'white').attr('stroke-width', 1.5);
    })
    .call(el => {
        el.selectAll('text').remove();
        el.append('text').attr('x', 8).attr('y', '0.31em').text((d) => participants.value[d.index].name).clone(true).lower().attr('fill', 'none').attr('stroke', 'white').attr('stroke-width', 3);
    })
    .transition()
    .duration(1000)
    .attr('transform', (d) => `translate(${x(d.x)}, ${y(d.y)})`);
}

const opponent = (participant: number, index: number) => {
    if (!graph.value) return "";
    const neighbours = graph.value.edges.get(graph.value.vertices[participant]);
    if (!neighbours) return "";
    return participants.value[neighbours[index].index].name;
}

d3.select(window).on("resize.updatechart", updateGraph);

onMounted(() => {
    setupGraph();
    updateGraph();
});

watch(participants, () => {
    updateGraph();
},
{ deep: true });

watch(graph, () => {
    updateGraph();
});
</script>

<style scoped>
.hidden {
  display: none !important;
}
.name {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin: 1rem;
}
.name label {
  width: 1rem;
}
.names {
  justify-content: center;
  height: 100vh;
  width: 40vw;
}
.graph {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 60vw;
}
.graph div {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 90%;
  height: 100%;
}
</style>
