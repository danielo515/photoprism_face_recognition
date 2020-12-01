const post = (url, params) =>
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(params),
        headers: { 'Content-Type': 'application/json' },
    }).then((x) => x.json());

const Get = (url) =>
    fetch(url, {
        method: 'GET',
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

/**
 * Returns a list of possible face matches from a given known face
 * @param {Object} param
 * @param {string} param.id the face id
 * @returns {Promise<{faces: {}, id: string}>} a promise with the possible face matches
 */
export const getFaceMatches = async ({ id }) => {
    const { result } = await Get(`/faces/${id}/matches`);
    return result;
};
