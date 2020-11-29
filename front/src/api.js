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

export const assignFacesToPerson = async ({ person_id, faces }) => {
    const result = await post(`people/${person_id}/faces`, { faces });
    return { result, faces };
};

/**
 * Creates a new person with an optional set of faces assigned to him/her
 * @param {Object} params
 * @param {string} params.name The name of the new person
 * @param {string[]} params.faces array of face IDs
 */
export const createPerson = async ({ name, faces }) => {
    const result = await post(`/people`, {
        name,
        faces,
    });
    return { result, faces };
};
