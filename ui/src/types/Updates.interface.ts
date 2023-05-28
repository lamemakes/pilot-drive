export interface Updates {
    update?: UpdateInfo
    error?: string
}

interface UpdateInfo {
    version: string
    completed: boolean
}