const getCoords = (x) => {
    const [top, right, bottom, left] = x.dataset.coord
        .replace(/[ ()]/g, "")
        .split(",")
        .map(Number);
    return { top, right, bottom, left };
};
const markFaces = () => {
    const facesDom = document.querySelector(".crop-face");
    const pos = getCoords(facesDom);
    console.log(pos);
    hyperHTML.bind(facesDom)`<div class='face-square' style=${{
        top: pos.top,
        left: pos.left,
    }} ></div>`;
    return facesDom;
};

const post = (url, params) =>
    fetch(url, {
        method: "POST",
        body: JSON.stringify(params),
        headers: { "Content-Type": "application/json" },
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

const assignSelectedFacesToPerson = async ({ person_id }) => {
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

const appState = {
    lastClicked: {
        id: null,
    },
    selectedFaces: new Set(),
    selectedPerson: null,
};

const selectFace = (evt) => {
    const node = evt.currentTarget;
    const data = node.dataset;
    id = node.id;
    node.classList.add("selected");
    appState.selectedFaces.add(id);
    toolbar();
};

const clearSelection = () => {
    document
        .querySelectorAll(".selected")
        .forEach((node) => node.classList.remove("selected"));
    appState.selectedFaces.clear();
};

const toolbar = () => {
    const toolbarDom = document.getElementById("toolbar");
    const options = hyperHTML.wire(
        appState,
        ":people-options"
    )`${server_data.people.map(
        (item) => hyperHTML.wire(item, ":option")`
        <option value=${item.id}>
            ${item.name}
        </option>
        `
    )}
    `;
    hyperHTML(toolbarDom)`
    <button onClick=${() =>
        assignSelectedFacesToPerson({
            person_id: appState.selectedPerson,
        })}>Assign selection to: </button>
    <select onchange=${(e) => (appState.selectedPerson = e.target.value)}>
        <option hidden selected> Select a person</option>
        ${options}
    </select>
    <button onClick=${clearSelection}>clear selection</button>
    `;
    toolbarDom.classList.add("toolbar-show");
};
