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
      <InputText
        :id="'participant' + participant.index"
        v-model="participant.name"
        @focus="participant.current = true"
        @blur="participant.current = false"
      /> vs.
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

import { Graph, Vertex } from '@/models/graph';
import graphs from '@/data/graphs';

const participantCount = ref(27)

class Participant {
  name: string
  index: number
  current: boolean
  constructor(name: string, index: number) {
    this.name = name
    this.index = index
    this.current = false
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

const drawing = ref<HTMLDivElement | null>(null);
const graph = ref<Graph>(graphs[27]);
let edgesGroup: d3.Selection<SVGGElement, unknown, null, undefined>;
let verticesGroup: d3.Selection<SVGGElement, unknown, null, undefined>;

let x: d3.ScaleTime<number, number, never>
let y: d3.ScaleLinear<number, number, never>
let line: d3.Line<{ date: Date; value: number }>

watch(participantCount, (newCount: number) => {
    graph.value = graphs[newCount] as Graph;
});

const setupGraph = () => {
    if (!drawing.value) return

    const margin = { top: 20, right: 30, bottom: 30, left: 40 }
    const width = drawing.value.clientWidth - margin.left - margin.right
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
    const width = drawing.value.clientWidth - margin.left - margin.right
    const height = drawing.value.clientHeight - margin.top - margin.bottom

    const size = Math.min(width, height) - 50;

    const y = d3.scaleLinear().nice().domain([minY, maxY]).range([height - (height - size)/2, (height - size)/2]);
    const x = d3.scaleLinear().nice().domain([minX, maxX]).range([(width - size)/2, width - (width - size)/2]);

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
    .attr("stroke", (d) => (participants.value[d.source.index].current || participants.value[d.target.index].current) ? "blue" : "currentColor")
    .attr("stroke-width", (d) => (participants.value[d.source.index].current || participants.value[d.target.index].current) ? 3 : 1.5);
  

  verticesGroup
    .selectAll('g')
    .data(vertices)
    .join('g')
    .each(function(parent) {
        d3.select(this)
          .selectAll('circle')
          .data([1])
          .join('circle')
          .attr('stroke', 'white')
          .attr('stroke-width', 1.5)
          .transition()
          .duration(1000)
          .attr('r', () => participants.value[parent.index].current ? 8 : 4)
          .attr('fill', () => participants.value[parent.index].current ? "blue" : "currentColor");
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
  overflow-y: auto;
  justify-content: center;
  height: 100vh;
  width: 40vw;
  padding-left: 1rem;
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
