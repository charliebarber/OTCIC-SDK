export function hyphenateStr(str) {
    return str.replace(/ +/g, '-').toLowerCase();
}