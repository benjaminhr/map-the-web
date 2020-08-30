import { URL } from "url";

export function isValidHttpUrl(string: string): boolean {
  let url;

  try {
    url = new URL(string);
  } catch (_) {
    return false;
  }

  return url.protocol === "http:" || url.protocol === "https:";
}

export function getOrigin(source: string): string {
  return new URL(source).origin;
}

export function sameDomain(source: string, href: string): boolean {
  return getOrigin(source) === getOrigin(href);
}
