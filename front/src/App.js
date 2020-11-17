import { toolbar } from './toolbar';

const getCoords = (x) => {
    const [top, right, bottom, left] = x.dataset.coord
        .replace(/[ ()]/g, '')
        .split(',')
        .map(Number);
    return { top, right, bottom, left };
};
const markFaces = () => {
    const facesDom = document.querySelector('.crop-face');
    const pos = getCoords(facesDom);
    console.log(pos);
    hyperHTML.bind(facesDom)`<div class='face-square' style=${{
        top: pos.top,
        left: pos.left,
    }} ></div>`;
    return facesDom;
};

const toggleClass = (id, className) => {
    const classes = document.getElementById(id).classList;
    classes.toggle(className);
};

const post = (url, params) =>
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: { 'Content-Type': 'application/json' },
    }).then((x) => x.json());

const assign_face_to_person = async ({ person_id, face_id }) => {
    const result = await post(`people/${person_id}/faces`, {
        faces: [face_id],
    });
    console.log(result);
};

const removeFacesFromDOM = (ids) => {
    ids.forEach((id) => document.getElementById(id).parentElement.remove());
};

export const assignSelectedFacesToPerson = async ({ person_id }) => {
    const faces = [...appState.selectedFaces];
    console.log({ faces });
    const result = await post(`people/${person_id}/faces`, { faces });
    removeFacesFromDOM(faces);
    appState.selectedFaces.clear();
    console.log(result);
};

const createPerson = async ({ name }) => {
    const result = await post(`/people`, {
        name,
        faces: [...appState.selectedFaces],
    });
    appState.selectedFaces.clear();
    console.log(result);
};

export const appState = {
    lastClicked: {
        id: null,
    },
    selectedFaces: new Set(),
    selectedPerson: null,
};

const selectFace = (evt) => {
    const node = evt.currentTarget;
    const data = node.dataset;
    const id = node.id;
    const classList = node.classList;
    if (appState.selectedFaces.has(id)) {
        classList.remove('selected');
        appState.selectedFaces.delete(id);
    } else {
        node.classList.add('selected');
        appState.selectedFaces.add(id);
    }
    toolbar();
};

window.selectFace = selectFace;

export const clearSelection = () => {
    document
        .querySelectorAll('.selected')
        .forEach((node) => node.classList.remove('selected'));
    appState.selectedFaces.clear();
};
