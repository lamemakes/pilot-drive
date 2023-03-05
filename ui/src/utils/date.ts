function getTwelveHourFormat(hours:number): string[] {
    let suffix = '';
    let prefix = '';
    if (hours > 12) {
        hours = hours - 12;
        suffix = "PM"
    } else if (hours === 0)  {
        hours = 12;
        suffix = "PM"
    } else {
        suffix = "AM";
    }

    return [`${prefix}${hours.toString()}`, ` ${suffix}`]
}

export function getTime(tfFormat:boolean): string {
    const date = new Date();
    const prefixString = (date.getHours() < 10 && tfFormat) ? '0' : '';
    const [hourString, suffixString] = (tfFormat) ? [date.getHours().toString(), ''] : getTwelveHourFormat(date.getHours());
    const minString = (date.getMinutes() < 10) ? `0${date.getMinutes().toString()}` : date.getMinutes().toString();

    return `${prefixString}${hourString}:${minString}${suffixString}`
}
