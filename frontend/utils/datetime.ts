import {DateTime} from 'luxon';

export function formatDate(iso: string, format: string) {
    return DateTime.fromISO(iso).setLocale('de').toFormat(format)
}

export function timeOfDay(iso: string) {
    return formatDate(iso, 'HH:mm')
}

export function dateOf(iso: string) {
    return formatDate(iso, 'dd LLLL yyyy')
}

export function sameDay(iso1: string, iso2: string): boolean {
    return formatDate(iso1, 'yyyy-MM-dd') === formatDate(iso2, 'yyyy-MM-dd')
}

export function moveDateByDiff(iso: string, diff1: string, diff2: string): string {
    const timeDiff = DateTime.fromISO(diff1)
        .diff(
            DateTime.fromISO(diff2)
        );
    console.log(diff1)
    console.log(diff2)
    console.log(timeDiff.toFormat('hh:mm:ss'));
    return DateTime.fromISO(iso).plus(timeDiff).toISODate() || "";
}