import { wire } from 'hyperhtml';

export default function Input({ label, name, onBlur = console.log, onChange }) {
    const blur = (e) => onBlur(e.currentTarget.value);
    const change = (e) => onChange(e.currentTarget.value);
    return wire()`
    <div class="grid grid-cols-3 gap-6">
    <div class="col-span-3 sm:col-span-2">
      <label for="${name}" class="block text-sm font-medium text-gray-700">
        ${label}
      </label>
      <div class="mt-1 flex rounded-md shadow-sm">
        <input onblur=${blur} onchange=${change} type="text" id="${name}" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md">
      </div>
    </div>
  </div>
    `;
}
