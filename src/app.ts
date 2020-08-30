import cheerio from "cheerio";
import fetch from "node-fetch";
import * as utils from "./utils";
import { Node, Graph } from "./Graph";

export async function run(
  initialURL = "https://benjaminhr.com",
  depth: number = 10,
  graph: Graph
): Promise<void> {
  try {
    const queue = [initialURL];

    let counter = 0;

    while (queue.length) {
      if (counter === depth) {
        break;
      }
      counter++;

      const currentURL = utils.getOrigin(queue.shift() as string);
      console.log("getting " + currentURL);
      const html = await getHTML(currentURL);
      const links = await getLinks(currentURL, html);
      const node = new Node(currentURL, links);
      graph.addNode(node);
      queue.push(...links);
    }
  } catch (error) {
    console.log(error);
  }
}

export async function getHTML(url: string): Promise<string> {
  if (!utils.isValidHttpUrl(url)) {
    throw new Error(`${url} is not a valid URL.`);
  }

  const request = await fetch(url);
  const html = await request.text();
  return html;
}

export function getLinks(sourceURL: string, html: string): Promise<string[]> {
  const parse = cheerio("a", html);
  const links = Object.values(parse)
    .map((object) => {
      return object?.attribs?.href && object.attribs.href.trim();
    })
    .filter(
      (href) =>
        Boolean(href) &&
        utils.isValidHttpUrl(href) &&
        !utils.sameDomain(sourceURL, href)
    )
    .map(utils.getOrigin);

  return Promise.resolve([...new Set(links)] as string[]);
}
