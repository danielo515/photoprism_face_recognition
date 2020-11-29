/**
 * @typedef Face
 * @property {string} id
 * @property {string} url
 */
export const appState = {
    lastClicked: {
        id: null,
    },
    selectedFaces: {
        list: new Set(),
        /** @type {Object.<string,Face>} */
        index: {},
    },
    selectedPerson: null,
};

const isPresent = (id) => appState.selectedFaces.list.has(id);

const getFaces = () => {
    const {
        selectedFaces: { list, index },
    } = appState;
    return { list, index };
};

const add = (id, url) => {
    appState.selectedFaces.index[id] = { id, url };
    appState.selectedFaces.list.add(id);
    return 'added';
};
const remove = (id) => {
    const { list, index } = getFaces();
    list.delete(id);
    delete index[id];
    return 'removed';
};

export function toggleFace({ id, url }) {
    const present = isPresent(id);
    if (present) return remove(id);
    return add(id, url);
}

export function addFace({ id, url }) {
    const present = isPresent(id);
    if (present) return;
    add(id, url);
}

export function removeFace({ id }) {
    const present = isPresent(id);
    if (!present) return;
    remove(id);
}

export function listFaces() {
    const { list, index } = getFaces();
    return [...list].map((id) => ({ id, url: index[id].url }));
}

export function clearFaces() {
    appState.selectedFaces.list.clear();
    appState.selectedFaces.index = {};
}

export const getFirstFace = () => {
    const { list, index } = getFaces();
    return index[list.entries().next().value[0]];
};

export const facesCount = () => {
    return appState.selectedFaces.list.size;
};
