import cheerio from "cheerio";
import fetch from "node-fetch";
import { URL } from "url";

class Node {
  public val: string;
  public links: string[];

  constructor(val: string, links: string[]) {
    this.val = val;
    this.links = links;
  }
}

class Graph {
  private graph: Node[] = [];

  addNode(node: Node) {
    this.graph.push(node);
  }

  getGraph(): Node[] {
    return this.graph;
  }
}

async function run(initialURL = "https://benjaminhr.com"): Promise<string> {
  const graph = new Graph();
  const queue = [initialURL];

  let counter = 0;

  while (queue.length) {
    if (counter === 20) {
      break;
    }
    counter++;

    const currentURL = queue.shift() as string;
    console.log("getting " + currentURL);
    const html = await getHTML(currentURL);
    const links = await getLinks(html);
    const node = new Node(currentURL, links);
    graph.addNode(node);
    queue.push(...links);
  }

  return JSON.stringify(graph.getGraph());
}

run().then(console.log);

async function getHTML(url: string): Promise<string> {
  if (!isValidHttpUrl(url)) {
    throw new Error(`${url} is not a valid URL.`);
  }

  const request = await fetch(url);
  const html = await request.text();
  return html;
}

function getLinks(html: string): Promise<string[]> {
  const parse = cheerio("a", html);
  const links = Object.values(parse)
    .map((object) => {
      return object.attribs && object.attribs.href;
    })
    .filter(Boolean && isValidHttpUrl);

  return Promise.resolve(links);
}

function isValidHttpUrl(string: string): boolean {
  let url;

  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }

  return url.protocol === "http:" || url.protocol === "https:";
}
