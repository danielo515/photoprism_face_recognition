/**
 * @typedef Face
 * @property {string} id
 * @property {string} url
 * @property {{top: number, left: number, bottom: number, right: number}} locations
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

/**
 *
 * @param {string} id
 * @param {string} url
 * @param {object} locations
 */
const add = (id, url, locations) => {
    appState.selectedFaces.index[id] = { id, url, locations };
    appState.selectedFaces.list.add(id);
    return 'added';
};
const remove = (id) => {
    const { list, index } = getFaces();
    list.delete(id);
    delete index[id];
    return 'removed';
};

/**
 * if it is present, remove from selected faces,
 * if it is not preset, add it
 * @param {Face} face
 */
export function toggleFace({ id, url, locations }) {
    const present = isPresent(id);
    if (present) return remove(id);
    return add(id, url, locations);
}

/**
 * Adds a face to the list of selected ones
 * @param {Face} face
 */
export function addFace({ id, url, locations }) {
    const present = isPresent(id);
    if (present) return;
    add(id, url, locations);
}

/**
 * Adds a face to the list of selected ones
 * @param {Face[]} faces
 */
export function addFaces(faces) {
    faces.forEach(addFace);
}

/**
 * Removes a face from the list of selected ones
 * @param {Face} face
 */
export function removeFace({ id }) {
    const present = isPresent(id);
    if (!present) return;
    remove(id);
}

/**
 * @returns {Face[]}
 */
export function listFaces() {
    const { list, index } = getFaces();
    return [...list].map((id) => ({
        id,
        url: index[id].url,
        locations: index[id].locations,
    }));
}
export const listFacesIds = () => {
    const { list } = getFaces();
    return [...list];
};

/**
 * Tells you if certain face has been selected
 * @param {string} faceId the face you want to check if it is selected
 */
export function isFaceSelected(faceId) {
    return isPresent(faceId);
}

export function clearFaces() {
    appState.selectedFaces.list.clear();
    appState.selectedFaces.index = {};
}

/**
 * Returns the first face on the list of selected faces
 * @returns {Face}
 */
export const getFirstFace = () => {
    const { list, index } = getFaces();
    return index[list.entries().next().value[0]];
};

export const facesCount = () => {
    return appState.selectedFaces.list.size;
};
