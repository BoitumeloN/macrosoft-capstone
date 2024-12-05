async function fetchStorageUnits() {
    const apiEndpoint = 'https://r6cxhs5fw6.execute-api.eu-west-1.amazonaws.com/Prod/storage_units';
    try {
        const response = await fetch(apiEndpoint);
        const units = await response.json();
        console.log(units);
        const unitsContainer = document.getElementById('storageUnits');
        unitsContainer.innerHTML = ''; // Clear previous units
        
        units.forEach(unit => {
            const unitDiv = document.createElement('div');
            unitDiv.className = 'unit';
            unitDiv.innerHTML = `
                <p>Unit Id: ${unit.unitid}</p>
                <p>Town: ${unit.Town}</p>
                <p>Unit Size: ${unit.Size}</p>
                <p>Status: ${unit.Status}</p>
                ${unit.Status === 'Available' ? `<button class="button" onclick="bookUnit('${unit.UnitId}')">Book Now</button>` : ''}
                ${unit.Status === 'Booked' ? `<button class="button" onclick="cancelRental('${unit.UnitId}')">Cancel</button>` : ''}
            `;
            unitsContainer.appendChild(unitDiv);
        });
    } catch (error) {
        console.error('Error fetching storage units:', error);
    }
}

async function bookUnit(unitId) {
    const apiEndpoint = `https://r6cxhs5fw6.execute-api.eu-west-1.amazonaws.com/Prod/storage-units/${unitId}`;
    try {
        const response = await fetch(apiEndpoint, { method: 'POST' });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list
    } catch (error) {
        console.error('Error booking unit:', error);
    }
}


async function updateStatus(unitId, newStatus) {
    const apiEndpoint = `https://r6cxhs5fw6.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'PUT', // Change method to PUT for updates
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after updating
    } catch (error) {
        console.error('Error updating status:', error);
    }
}


async function cancelRental(unitId) {
    const apiEndpoint = `https://r6cxhs5fw6.execute-api.eu-west-1.amazonaws.com/Prod/storage-units/${unitId}`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${yourAuthToken}` // Include your Cognito token
            }
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after cancellation
    } catch (error) {
        console.error('Error canceling rental:', error);
    }
}

// Initial fetch
fetchStorageUnits();