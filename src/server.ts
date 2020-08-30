import WebSocket from "ws";
import { Node, Graph } from "./Graph";
import { run } from "./app";

export default class Server {
  private port: number;
  private server: WebSocket.Server;
  private ws: any;
  private graph: Graph;

  constructor(port: number = 8080) {
    this.port = port;
    this.graph = new Graph(this);
    this.server = new WebSocket.Server({ port: this.port });
    this.server.on("connection", (ws) => {
      this.ws = ws;

      ws.on("message", (msg) => {
        const data = JSON.parse(msg as string);
        const url = data.url;
        const depth = data.depth;
        run(url, depth, this.graph);
      });
    });
  }

  sendMessage(node: Node) {
    this.ws.send(JSON.stringify(node));
  }
}
