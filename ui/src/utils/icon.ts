export function getIconUrl(url:string) {
    return new URL(url, import.meta.url).href
}