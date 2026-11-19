
// const API_BASE = "http://127.0.0.1:8000";
const API_BASE = "https://contact-management-r4in.onrender.com";
const PAGE_SIZE = 5;


// ======================================
// 1. DATA CONFIGURATION
// ======================================

const modules = {

    contacts: {
        endpoint: "/contacts",
        id: "contact_id",
        title: "Contacts",
        table: "contactsTable",
        search: "contactsSearch",
        pagination: "contactsPagination",

        fields: [
            {
                name: "name",
                label: "Name",
                type: "text",
                required: true
            },
            {
                name: "email",
                label: "Email",
                type: "email",
                required: true
            },
            {
                name: "company_id",
                label: "Company",
                type: "select",
                source: "companies",
                required: false
            },
            {
                name: "phone",
                label: "Phone",
                type: "tel",
                required: true
            }
        ],

        columns: [
            "contact_id",
            "name",
            "email",
            "phone",
            "company_id"
        ],

        searchable: [
            "name",
            "email",
            "phone",
            "company_id"
        ]
    },


    companies: {
        endpoint: "/companies",
        id: "company_id",
        title: "Companies",
        table: "companiesTable",
        search: "companiesSearch",
        pagination: "companiesPagination",

        fields: [
            {
                name: "name",
                label: "Company Name",
                type: "text",
                required: true
            },
            {
                name: "website",
                label: "Website",
                type: "url",
                required: true
            },
            {
                name: "phone",
                label: "Phone",
                type: "tel",
                required: true
            }
        ],

        columns: [
            "company_id",
            "name",
            "website",
            "phone"
        ],

        searchable: [
            "name",
            "website",
            "phone"
        ]
    },


    phones: {
        endpoint: "/phones",
        id: "phone_id",
        title: "Phones",
        table: "phonesTable",
        search: "phonesSearch",
        pagination: "phonesPagination",

        fields: [
            {
                name: "contact_id",
                label: "Contact",
                type: "select",
                source: "contacts",
                required: true
            },
            {
                name: "phone",
                label: "Phone Number",
                type: "tel",
                required: true
            }
        ],

        columns: [
            "phone_id",
            "contact_id",
            "phone"
        ],

        searchable: [
            "phone",
            "contact_id"
        ]
    },


    notes: {
        endpoint: "/notes",
        id: "notes_id",
        title: "Notes",
        table: "notesTable",
        search: "notesSearch",
        pagination: "notesPagination",

        fields: [
            {
                name: "contact_id",
                label: "Contact",
                type: "select",
                source: "contacts",
                required: true
            },
            {
                name: "notes",
                label: "Note",
                type: "textarea",
                required: true
            }
        ],

        columns: [
            "notes_id",
            "contact_id",
            "notes"
        ],

        searchable: [
            "notes",
            "contact_id"
        ]
    }

};


// ======================================
// 2. APPLICATION STATE
// ======================================

const dataStore = {
    contacts: [],
    companies: [],
    phones: [],
    notes: []
};

const currentPages = {
    contacts: 1,
    companies: 1,
    phones: 1,
    notes: 1
};

let activeModule = null;
let editingId = null;


// ======================================
// 3. DOM ELEMENTS
// ======================================

const modal = document.getElementById("modal");
const modalTitle = document.getElementById("modalTitle");
const recordForm = document.getElementById("recordForm");
const formFields = document.getElementById("formFields");

const closeModalBtn = document.getElementById("closeModal");
const cancelBtn = document.getElementById("cancelBtn");

const toast = document.getElementById("toast");


// ======================================
// 4. HELPER FUNCTIONS
// ======================================

function escapeHTML(value) {

    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);

}


function getSingularName(moduleName) {

    const names = {
        contacts: "Contact",
        companies: "Company",
        phones: "Phone",
        notes: "Note"
    };

    return names[moduleName] || moduleName;

}


function showToast(message, type = "success") {

    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.className = "toast";
    }, 3000);

}


function getErrorMessage(error) {

    if (Array.isArray(error)) {

        return error
            .map(item => item.msg || "Invalid input")
            .join(", ");

    }

    return String(error || "Something went wrong");

}


// ======================================
// 5. API REQUEST WITH JWT AUTHENTICATION
// ======================================

async function apiRequest(url, options = {}) {

    const token = sessionStorage.getItem("access_token");

    if (!token) {

        window.location.replace("login.html");

        throw new Error("Please login first.");

    }

    try {

        const headers = {
            ...options.headers,
            "Authorization": `Bearer ${token}`
        };

        if (options.body) {
            headers["Content-Type"] = "application/json";
        }

        const response = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers
        });

        const responseText = await response.text();

        let result = null;

        if (responseText) {

            try {
                result = JSON.parse(responseText);
            } catch {
                result = responseText;
            }

        }

        if (response.status === 401) {

            sessionStorage.removeItem("access_token");

            window.location.replace("login.html");

            throw new Error("Session expired. Please login again.");

        }

        if (!response.ok) {

            const message =
                result?.detail ||
                result?.message ||
                response.statusText;

            throw new Error(getErrorMessage(message));

        }

        return result;

    } catch (error) {

        if (error instanceof TypeError) {

            throw new Error(
                "Backend connection failed. Please check your FastAPI server."
            );

        }

        throw error;

    }

}


// ======================================
// 6. FETCH MODULE DATA
// ======================================

async function fetchModuleData(moduleName) {

    const config = modules[moduleName];

    try {

        const result = await apiRequest(config.endpoint);

        dataStore[moduleName] = Array.isArray(result)
            ? result
            : [];

        renderTable(moduleName);

        updateDashboard();

        return dataStore[moduleName];

    } catch (error) {

        dataStore[moduleName] = [];

        renderTable(moduleName);

        updateDashboard();

        if (error.message !== "Please login first.") {

            showToast(
                `${config.title}: ${error.message}`,
                "error"
            );

        }

        return [];

    }

}


async function loadAllData() {

    const names = Object.keys(modules);

    await Promise.all(
        names.map(name => fetchModuleData(name))
    );

}


// ======================================
// 7. DASHBOARD STATISTICS
// ======================================

function updateDashboard() {

    document.getElementById("totalContacts").textContent =
        dataStore.contacts.length;

    document.getElementById("totalCompanies").textContent =
        dataStore.companies.length;

    document.getElementById("totalPhones").textContent =
        dataStore.phones.length;

    document.getElementById("totalNotes").textContent =
        dataStore.notes.length;

}


// ======================================
// 8. SEARCH
// ======================================

function getFilteredData(moduleName) {

    const config = modules[moduleName];

    const searchElement = document.getElementById(config.search);

    if (!searchElement) {
        return dataStore[moduleName];
    }

    const searchValue = searchElement.value.trim().toLowerCase();

    if (!searchValue) {
        return dataStore[moduleName];
    }

    return dataStore[moduleName].filter(record => {

        return config.searchable.some(field => {

            return String(record[field] ?? "")
                .toLowerCase()
                .includes(searchValue);

        });

    });

}


// ======================================
// 9. TABLE RENDERING
// ======================================

function renderTable(moduleName) {

    const config = modules[moduleName];

    const container = document.getElementById(config.table);

    if (!container) return;

    const filteredData = getFilteredData(moduleName);

    const totalPages = Math.max(
        1,
        Math.ceil(filteredData.length / PAGE_SIZE)
    );

    currentPages[moduleName] = Math.min(
        currentPages[moduleName],
        totalPages
    );

    const startIndex =
        (currentPages[moduleName] - 1) * PAGE_SIZE;

    const pageData = filteredData.slice(
        startIndex,
        startIndex + PAGE_SIZE
    );


    if (filteredData.length === 0) {

        container.innerHTML = `
            <div class="table-container">
                <table>
                    <tbody>
                        <tr>
                            <td class="empty-row">
                                No records found.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;

    } else {

        const headers = config.columns.map(column => `
            <th>
                ${escapeHTML(column.replaceAll("_", " ").toUpperCase())}
            </th>
        `).join("");


        const rows = pageData.map(record => {

            const id = record[config.id];

            const cells = config.columns.map(column => `
                <td>${escapeHTML(record[column])}</td>
            `).join("");


            return `
                <tr>

                    ${cells}

                    <td>
                        <div class="action-buttons">

                            <button
                                class="edit-btn"
                                data-action="edit"
                                data-id="${escapeHTML(id)}">
                                Edit
                            </button>

                            <button
                                class="delete-btn"
                                data-action="delete"
                                data-id="${escapeHTML(id)}">
                                Delete
                            </button>

                        </div>
                    </td>

                </tr>
            `;

        }).join("");


        container.innerHTML = `
            <div class="table-container">

                <table>

                    <thead>
                        <tr>
                            ${headers}
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        ${rows}
                    </tbody>

                </table>

            </div>
        `;

    }

    renderPagination(
        moduleName,
        filteredData.length,
        totalPages
    );

}


// ======================================
// 10. PAGINATION
// ======================================

function renderPagination(moduleName, totalRecords, totalPages) {

    const config = modules[moduleName];

    const container = document.getElementById(config.pagination);

    if (!container) return;

    if (totalRecords <= PAGE_SIZE) {

        container.innerHTML = "";

        return;

    }

    const currentPage = currentPages[moduleName];

    container.innerHTML = `

        <div class="pagination">

            <button
                data-page-action="previous"
                data-module="${moduleName}"
                ${currentPage === 1 ? "disabled" : ""}>
                Previous
            </button>

            <span>
                Page ${currentPage} of ${totalPages}
            </span>

            <button
                data-page-action="next"
                data-module="${moduleName}"
                ${currentPage === totalPages ? "disabled" : ""}>
                Next
            </button>

        </div>

    `;

}


// ======================================
// 11. NAVIGATION
// ======================================

function showSection(sectionName) {

    document.querySelectorAll(".page-section").forEach(section => {

        section.classList.add("hidden");

    });

    const selectedSection = document.getElementById(sectionName);

    if (!selectedSection) return;

    selectedSection.classList.remove("hidden");


    document.querySelectorAll(".nav-btn").forEach(button => {

        button.classList.toggle(
            "active",
            button.dataset.section === sectionName
        );

    });


    const titles = {

        dashboard: [
            "Dashboard",
            "Welcome to your Contact Management System"
        ],

        contacts: [
            "Contacts",
            "Manage your contacts"
        ],

        companies: [
            "Companies",
            "Manage companies"
        ],

        phones: [
            "Phones",
            "Manage contact phone numbers"
        ],

        notes: [
            "Notes",
            "Manage contact notes"
        ]

    };


    if (!titles[sectionName]) return;

    document.getElementById("pageTitle").textContent =
        titles[sectionName][0];

    document.getElementById("pageSubtitle").textContent =
        titles[sectionName][1];

}


// ======================================
// 12. DROPDOWN OPTIONS
// ======================================

function getDropdownOptions(source, selectedValue) {

    const records = dataStore[source] || [];

    const config = modules[source];

    if (!config) return "";

    return records.map(record => {

        const id = record[config.id];

        const label =
            record.name ||
            record.notes ||
            record.phone ||
            `Record ${id}`;

        return `
            <option
                value="${escapeHTML(id)}"
                ${String(id) === String(selectedValue) ? "selected" : ""}>

                ${escapeHTML(label)} (ID: ${escapeHTML(id)})

            </option>
        `;

    }).join("");

}


// ======================================
// 13. OPEN ADD / EDIT MODAL
// ======================================

function openModal(moduleName, record = null) {

    if (!modules[moduleName]) return;

    activeModule = moduleName;

    editingId = record
        ? record[modules[moduleName].id]
        : null;

    const config = modules[moduleName];

    modalTitle.textContent = record
        ? `Edit ${getSingularName(moduleName)}`
        : `Add ${getSingularName(moduleName)}`;


    formFields.innerHTML = config.fields.map(field => {

        const value = record
            ? record[field.name] ?? ""
            : "";


        if (field.type === "select") {

            return `
                <div class="form-group">

                    <label for="${field.name}">
                        ${escapeHTML(field.label)}
                    </label>

                    <select
                        id="${field.name}"
                        name="${field.name}"
                        ${field.required ? "required" : ""}>

                        <option value="">
                            Select ${escapeHTML(field.label)}
                        </option>

                        ${getDropdownOptions(field.source, value)}

                    </select>

                </div>
            `;

        }


        if (field.type === "textarea") {

            return `
                <div class="form-group">

                    <label for="${field.name}">
                        ${escapeHTML(field.label)}
                    </label>

                    <textarea
                        id="${field.name}"
                        name="${field.name}"
                        ${field.required ? "required" : ""}>${escapeHTML(value)}</textarea>

                </div>
            `;

        }


        return `
            <div class="form-group">

                <label for="${field.name}">
                    ${escapeHTML(field.label)}
                </label>

                <input
                    type="${field.type}"
                    id="${field.name}"
                    name="${field.name}"
                    value="${escapeHTML(value)}"
                    ${field.required ? "required" : ""}
                >

            </div>
        `;

    }).join("");


    modal.classList.remove("hidden");

}


// ======================================
// 14. CLOSE MODAL
// ======================================

function closeModal() {

    modal.classList.add("hidden");

    recordForm.reset();

    activeModule = null;

    editingId = null;

}


closeModalBtn.addEventListener("click", closeModal);

cancelBtn.addEventListener("click", closeModal);


// ======================================
// 15. ADD / UPDATE RECORD
// ======================================

recordForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    if (!activeModule) return;

    const moduleName = activeModule;

    const config = modules[moduleName];

    const formData = new FormData(recordForm);

    const recordData = {};


    config.fields.forEach(field => {

        let value = formData.get(field.name);

        if (field.type === "select") {

            value = value === "" ? null : Number(value);

        }

        recordData[field.name] = value;

    });


    const isEditing = editingId !== null;

    const url = isEditing
        ? `${config.endpoint}/${editingId}`
        : config.endpoint;

    const method = isEditing ? "PUT" : "POST";


    const saveButton = document.getElementById("saveBtn");

    saveButton.disabled = true;

    saveButton.textContent = "Saving...";


    try {

        await apiRequest(url, {

            method: method,

            body: JSON.stringify(recordData)

        });


        showToast(
            `${getSingularName(moduleName)} ${
                isEditing ? "updated" : "created"
            } successfully!`
        );


        closeModal();

        await refreshRelatedData(moduleName);


    } catch (error) {

        showToast(error.message, "error");

    } finally {

        saveButton.disabled = false;

        saveButton.textContent = "Save";

    }

});


// ======================================
// 16. REFRESH RELATED DATA
// ======================================

async function refreshRelatedData(moduleName) {

    await fetchModuleData(moduleName);


    if (moduleName === "contacts") {

        await Promise.all([
            fetchModuleData("phones"),
            fetchModuleData("notes")
        ]);

    }

}


// ======================================
// 17. DELETE RECORD
// ======================================

async function deleteRecord(moduleName, id) {

    const config = modules[moduleName];

    const confirmed = confirm(
        `Are you sure you want to delete this ${getSingularName(moduleName).toLowerCase()}?`
    );

    if (!confirmed) return;


    try {

        await apiRequest(`${config.endpoint}/${id}`, {

            method: "DELETE"

        });


        showToast(
            `${getSingularName(moduleName)} deleted successfully!`
        );


        await refreshRelatedData(moduleName);


    } catch (error) {

        showToast(error.message, "error");

    }

}


// ======================================
// 18. TABLE BUTTON EVENTS
// ======================================

Object.keys(modules).forEach(moduleName => {

    const config = modules[moduleName];

    const table = document.getElementById(config.table);

    if (!table) return;


    table.addEventListener("click", function(event) {

        const button = event.target.closest(
            "button[data-action]"
        );

        if (!button) return;

        const id = button.dataset.id;

        const record = dataStore[moduleName].find(item => {

            return String(item[config.id]) === String(id);

        });

        if (!record) return;


        if (button.dataset.action === "edit") {

            openModal(moduleName, record);

        }


        if (button.dataset.action === "delete") {

            deleteRecord(moduleName, id);

        }

    });

});


// ======================================
// 19. PAGINATION EVENTS
// ======================================

Object.keys(modules).forEach(moduleName => {

    const config = modules[moduleName];

    const pagination = document.getElementById(config.pagination);

    if (!pagination) return;


    pagination.addEventListener("click", function(event) {

        const button = event.target.closest(
            "button[data-page-action]"
        );

        if (!button) return;


        const action = button.dataset.pageAction;

        if (action === "next") {

            currentPages[moduleName]++;

        }

        if (action === "previous") {

            currentPages[moduleName]--;

        }


        renderTable(moduleName);

    });

});


// ======================================
// 20. SEARCH EVENTS
// ======================================

Object.keys(modules).forEach(moduleName => {

    const config = modules[moduleName];

    const search = document.getElementById(config.search);

    if (!search) return;


    search.addEventListener("input", function() {

        currentPages[moduleName] = 1;

        renderTable(moduleName);

    });

});


// ======================================
// 21. NAVIGATION EVENTS
// ======================================

document.querySelectorAll(".nav-btn").forEach(button => {

    button.addEventListener("click", function() {

        showSection(button.dataset.section);

    });

});


// ======================================
// 22. ADD BUTTON EVENTS
// ======================================

document.querySelectorAll(".add-btn").forEach(button => {

    button.addEventListener("click", function() {

        openModal(button.dataset.add);

    });

});


// ======================================
// 23. INITIALIZE APPLICATION
// ======================================

async function initializeApp() {

    showSection("dashboard");

    await loadAllData();

}


initializeApp();
