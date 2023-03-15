import { SettingsStore } from "../stores/SettingsStore";

// Lumin values are for text on either the primary/secondary color
export enum ColorVars {
    ACCENT = "--accent-color",
    PRIMARY = "--primary-color",
    SECONDARY = "--secondary-color",
    PRIMARY_LUMIN = "--primary-lumin",
    SECONDARY_LUMIN = "--secondary-lumin"
}

// The dark/light values to be used for text lumin values
export const DARK = [0, 0, 0]
export const LIGHT = [255, 255, 255]

/**
 * Returns either a light or dark contrasting color based on an input color.
 * For more info, see https://stackoverflow.com/questions/946544/good-text-foreground-color-for-a-given-background-color/946734#946734
 *
 * @param color - A color in the form of an RGB array
 * @returns either a light or dark color to constrast the input
 *
 */
export function getContrastingColor(color: number[]): number[] {

    return ((color[0] * 0.299 + color[1] * 0.587 + color[2] * 0.114) > 186) ? DARK : LIGHT;
}

export function getRgbString(color: number[]): string {
    return `rgb(${color.join(',')})`
}

/**
 * Returns either a light or dark contrasting color based on an input color.
 * For more info, see https://stackoverflow.com/questions/946544/good-text-foreground-color-for-a-given-background-color/946734#946734
 *
 * @param color - A color in the form of an RGB array
 * @returns either a light or dark color to constrast the input
 *
 */
export function setGlobalTheme(newTheme: string): void {
    console.log("SETTING THEME: " + newTheme);
    let root = document.querySelector(':root') as HTMLElement;

    let selectedTheme = SettingsStore.themes.find(theme => theme.name == newTheme);

    if (selectedTheme === undefined) {
        console.error(`Failed to find specified theme: "${newTheme}"!`); // TODO: Toast/Notifications
        return
    }

    root.style.setProperty(ColorVars.ACCENT, getRgbString(selectedTheme.accent));
    root.style.setProperty(ColorVars.PRIMARY, getRgbString(selectedTheme.primary));
    root.style.setProperty(ColorVars.SECONDARY, getRgbString(selectedTheme.secondary))

    console.log("PRIMARY LUMIN")
    console.log(getContrastingColor(selectedTheme.primary))
    console.log("SECONDARY LUMIN")
    console.log(getContrastingColor(selectedTheme.secondary))

    root.style.setProperty(ColorVars.PRIMARY_LUMIN, getRgbString(getContrastingColor(selectedTheme.primary)));
    root.style.setProperty(ColorVars.SECONDARY_LUMIN, getRgbString(getContrastingColor(selectedTheme.secondary)));
}

/**
 * Handles inverting icons to the reflect the lumin values. Assumes icon images are black.
 *
 * @param className - the class pertaining to the <img> tags in question
 * @param intendedLumin - either the PRIMARY_LUMIN or SECONDARY_LUMIN values.
 *
 */
export function handleIconLumin(className: string, intendedLumin: ColorVars): void {
    let isDarkLumin = true; // Fallback value is root can't be queried for some reason.

    const icons = Array.from(document.getElementsByClassName(className));
    console.log("ICONS:");
    console.log(icons)
    const root = document.querySelector(':root');

    if (root) {
        const targetLumin = window.getComputedStyle(root).getPropertyValue(intendedLumin);
        isDarkLumin = (targetLumin == getRgbString(DARK));
    }

    for (let i = 0; i < icons.length; i++){
        console.log("IS DARK LUMIN: " + isDarkLumin);
        if (isDarkLumin) {
            (icons[i] as HTMLImageElement).style.webkitFilter = "invert(0%)";
        } else {
            (icons[i] as HTMLImageElement).style.webkitFilter = "invert(100%)";
        }
    }
}