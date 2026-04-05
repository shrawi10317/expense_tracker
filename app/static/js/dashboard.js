let editId = null;

// Load all expenses on page load
document.addEventListener("DOMContentLoaded", loadExpenses);

async function loadExpenses() {
    try {
        const response = await fetch('/api/expenses');
        if (!response.ok) throw new Error("Failed to load expenses");
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error(error);
        alert("Error loading expenses");
    }
}

// Save or Edit expense
async function saveExpense() {
    const amount = parseFloat(document.getElementById("amount").value);
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value;

    if (!amount || !category) {
        alert("Amount and Category are required!");
        return;
    }

    let url = "/api/add-expense";
    let method = "POST";

    if (editId) {
        url = `/api/edit-expense/${editId}`;
        method = "PUT";
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount, category, description })
        });
        if (!response.ok) throw new Error("Failed to save expense");

        const data = await response.json();
        updateUI(data);

        editId = null;
        document.getElementById("expenseForm").reset();
    } catch (error) {
        console.error(error);
        alert("Error saving expense");
    }
}

// Delete expense
async function deleteExpense(id) {
    if (!confirm("Are you sure?")) return;
    try {
        const response = await fetch(`/api/delete-expense/${id}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Failed to delete expense");
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error(error);
        alert("Error deleting expense");
    }
}

// Edit expense
function editExpense(id) {
    editId = id;
    const li = document.querySelector(`#list li[data-id='${id}']`);
    document.getElementById("amount").value = li.dataset.amount;
    document.getElementById("category").value = li.dataset.category;
    document.getElementById("description").value = li.dataset.description;
}

// Update UI
function updateUI(data) {
    const list = document.getElementById("list");
    const totalEl = document.getElementById("total");
    list.innerHTML = "";
    let total = 0;

    data.expenses.forEach(exp => {
        total += exp.amount;
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.dataset.id = exp.id;
        li.dataset.amount = exp.amount;
        li.dataset.category = exp.category;
        li.dataset.description = exp.description;

        li.innerHTML = `
            ${exp.category} - ₹${exp.amount} - ${exp.description || ''}
            <div>
                <button class="btn btn-sm btn-primary me-1" onclick="editExpense(${exp.id})">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteExpense(${exp.id})">❌</button>
            </div>
        `;
        list.appendChild(li);
    });

    totalEl.innerText = total.toFixed(2);
}

// Filter by date
async function filterExpenses() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    if (!start && !end) {
        alert("Please select at least one date!");
        return;
    }

    // Build query params
    const startParam = start || "";
    const endParam = end || "";

    try {
        const response = await fetch(`/api/filter-expenses?start=${startParam}&end=${endParam}`);
        if (!response.ok) throw new Error("Failed to filter expenses");

        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error(error);
        alert("Error filtering expenses");
    }
}

// Reset filter button
function resetFilter() {
    document.getElementById("startDate").value = "";
    document.getElementById("endDate").value = "";
    loadExpenses();
}
// Monthly report
async function monthlyReport() {
    const month = document.getElementById("month").value;
    if (!month) {
        alert("Select a month first!");
        return;
    }

    try {
        const response = await fetch(`/api/monthly-report?month=${month}`);
        if (!response.ok) throw new Error("Failed to generate report");
        const data = await response.json();

        const list = document.getElementById("list");
        list.innerHTML = "";
        for (let category in data.report) {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.innerText = `${category} - ₹${data.report[category]}`;
            list.appendChild(li);
        }

        document.getElementById("total").innerText = data.total.toFixed(2);
    } catch (error) {
        console.error(error);
        alert("Error generating monthly report");
    }
}