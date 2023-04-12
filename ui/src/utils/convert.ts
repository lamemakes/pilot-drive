export function kilometerToMile(kilometers: number) {
    return kilometers * 0.6213712
}

export function litreToGallon(litres: number) {
    return litres / 4.5
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