import newUserBtn from './person-btn';
import { appState, assignSelectedFacesToPerson, clearSelection } from './App';

export const toolbar = () => {
    const toolbarDom = document.getElementById('toolbar');
    const options = hyperHTML.wire(
        appState,
        ':people-options',
    )`${server_data.people.map(
        (item) => hyperHTML.wire(item, ':option')`
        <option value=${item.id}>
            ${item.name}
        </option>
        `,
    )}
    `;
    hyperHTML(toolbarDom)`
    <button class="button" onClick=${() =>
        assignSelectedFacesToPerson({
            person_id: appState.selectedPerson,
        })}>Assign selection to: </button>
    <select onchange=${(e) => (appState.selectedPerson = e.target.value)}>
        <option hidden selected> Select a person</option>
        ${options}
    </select>
    ${newUserBtn({ onClick: console.log })}
    <button onClick=${clearSelection}>clear selection</button>
    `;
    if (appState.selectedFaces.size > 0)
        toolbarDom.classList.add('toolbar-show');
    else toolbarDom.classList.remove('toolbar-show');
};
