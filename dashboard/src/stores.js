import { writable } from 'svelte/store';
import { apps } from './data';
import { hyphenateStr } from './utils';

const initialLastApp = hyphenateStr(apps[0].name);

export const lastApp = writable(initialLastApp);