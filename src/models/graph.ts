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
    constructor(vertices: Vertex[], edges: Map<Vertex, Vertex[]>) {
        this.vertices = vertices
        this.edges = edges
    }
}
