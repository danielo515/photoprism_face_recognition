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
    const result = (
        await fetch(`people/${person_id}/face/${face_id}`, { method: "POST" })
    ).json();
    console.log(result);
};

const createPerson = async ({ name }) => {
    const result = await post(`/people`, { name });
    console.log(result);
};
