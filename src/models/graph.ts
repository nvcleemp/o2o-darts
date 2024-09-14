export class Vertex {
  index: number
  x: number
  y: number
  constructor(index: number, x: number, y: number) {
    this.index = index
    this.x = x
    this.y = y
  }
}

export class Graph {
  vertices: Vertex[]
  edges: Map<Vertex, Vertex[]>
  arced?: Map<Vertex, Map<Vertex, number>>
  constructor(
    vertices: Vertex[],
    edges: Map<Vertex, Vertex[]>,
    arced?: Map<Vertex, Map<Vertex, number>>
  ) {
    this.vertices = vertices
    this.edges = edges
    this.arced = arced
  }

  getArcedWeight(from: Vertex, to: Vertex): number {
    if (this.arced) {
      return this.arced.get(from)?.get(to) || 0
    } else {
      return 0
    }
  }

  hasArcWeight(): boolean {
    return this.arced !== undefined
  }
}
