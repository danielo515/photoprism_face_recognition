import { removeFacesFromDOM } from './App';
import { appState } from './appState';

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
