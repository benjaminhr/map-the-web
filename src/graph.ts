import Server from "./server";

export class Node {
  public val: string;
  public links: string[];

  constructor(val: string, links: string[]) {
    this.val = val;
    this.links = links;
  }
}

export class Graph {
  private graph: Node[] = [];
  private server: Server;

  constructor(server: Server) {
    this.server = server;
  }

  addNode(node: Node) {
    this.server.sendMessage(node);
    this.graph.push(node);
  }

  getGraph(): Node[] {
    return this.graph;
  }
}
