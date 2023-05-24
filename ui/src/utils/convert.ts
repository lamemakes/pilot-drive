// Likely a library that makes this easier somewhere. Conversions pulled from NIST:
// https://www.nist.gov/pml/owm/approximate-conversions-us-customary-measures-metric

export function kilometerToMile(kilometers: number) {
    return kilometers * 0.6213712
}

export function celsiusToFahrenheit(celsius: number) {
    return (celsius * (9/5)) + 32
}

export function literToGallon(litres: number) {
    return litres / 3.79
}

export function gramToOunce(grams: number) {
    return grams / 28.35
}

export function kilogramToPound(kilograms: number) {
    return kilograms / 0.45
}

// Does not accent hex shortcut strings, only 6 char.
function hexToRgbA(hex: string){
    if(/^#([A-Fa-f0-9]{3}){2}$/.test(hex)){
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgb(${r}, ${g}, ${b})`;
    }
    throw new Error('Detected invalid hex while attempting to convert hex to RGB!');
}