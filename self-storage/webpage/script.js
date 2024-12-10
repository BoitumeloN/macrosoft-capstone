const apiEndpoint = 'https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod';

async function fetchStorageUnits() {
    const apiEndpoint = 'https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units';
    try {
        const response = await fetch(apiEndpoint);
        const units = await response.json();
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
                ${unit.Status === 'Available' ? `<button class="button" onclick="bookUnit('${unit.unitid}')")">Book Now</button>` : ''}
                ${unit.Status === 'Reserved' ? `<button class="button" onclick="cancelRental('${unit.unitid}')">Cancel</button>` : ''}
            `;
            unitsContainer.appendChild(unitDiv);
        });
    } catch (error) {
        console.error('Error fetching storage units:', error);
    }
}

let currentUnitId = null; // To store the current unitId
async function bookUnit(unitId) {
    // const authToken = await checkAuthStatus();
    // if (!authToken) {
    //     login(); // Redirect to login if not authenticated
    //     return;
    // }
    currentUnitId = unitId; // Store the unitId for later use
    document.getElementById('bankingModal').style.display = 'block'; // Show the modal

    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${currentUnitId}`;
    try {
        const response = await fetch(apiEndpoint, { method: 'POST' });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list
    } catch (error) {
        console.error('Error booking unit:', error);
    }

}
    // Show the modal to ask for banking details

function submitBankingDetails() {
    const accountNumber = document.getElementById('accountNumber').value;
    const routingNumber = document.getElementById('routingNumber').value;
    const exDate = document.getElementById('exDate').value;

    if (!accountNumber || !routingNumber) {
        alert("Please fill in all fields.");
        return;
    }

    const bankingDetails = {
        accountNumber: accountNumber,
        routingNumber: routingNumber,
        exDate: exDate,
    };
    const authToken = localStorage.getItem('authToken'); // Retrieve the token again
    const apiEndpoint = `https://azj8qg4dqh.execute-api.eu-west-1.amazonaws.com/Prod/${currentUnitId}`;
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bankingDetails)
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
        fetchStorageUnits(); // Refresh the list
        closeModal(); // Close the modal
    })
    .catch(error => {
        console.error('Error booking unit:', error);
    });
    closeModal();
}

function closeModal() {
    document.getElementById('bankingModal').style.display = 'none';
    document.getElementById('accountNumber').value = ''; // Clear input fields
    document.getElementById('routingNumber').value = '';
}


async function updateStatus(unitId, newStatus) {
    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}/status/${newStatus}`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'PUT', // Change method to PUT for updates
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer 0` // Include your Cognito token
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
    const authToken = await checkAuthStatus();
    if (!authToken) {
        login(); // Redirect to login if not authenticated
        return;
    }

    const apiEndpoint = `https://y1ceks7lrg.execute-api.eu-west-1.amazonaws.com/Prod/storage_units/${unitId}/cancel`;
    try {
        const response = await fetch(apiEndpoint, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${authToken}` // Include your Cognito token
            }
        });
        const result = await response.json();
        alert(result.message);
        fetchStorageUnits(); // Refresh the list after cancellation
    } catch (error) {
        console.error('Error canceling rental:', error);
    }
}

function login() {
    // Redirect to the Cognito login page
    const cognitoLoginUrl = 'https://eu-west-1pv6wty3qq.auth.eu-west-1.amazoncognito.com/login?client_id=44t95jhbmn74mjqh99tn2lbhih&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https%3A%2F%2Fmain.d2v7oqvnc2mjzz.amplifyapp.com%2F';
    window.location.href = cognitoLoginUrl;
}


function signout() {
    // Clear the authentication token and redirect to the home page
    localStorage.removeItem('authToken');
    window.location.href = '/';
}

async function checkAuthStatus() {
    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
        return null; // Return null if not authenticated
    }

    try {
        const response = await fetch(`${apiEndpoint}/validateAuthToken`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            }
        });

        if (response.status === 200) {
            document.querySelector('.login-button').style.display = 'none';
            document.querySelector('.signout-button').style.display = 'block';
            return authToken; // Return the token if valid
        } else {
            document.querySelector('.login-button').style.display = 'block';
            document.querySelector('.signout-button').style.display = 'none';
            return null; // Return null if not valid
        }
    } catch (error) {
        console.error('Error checking auth status:', error);
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
        return null; // Return null on error
    }
}
// Initial fetch and check authentication status
fetchStorageUnits();
checkAuthStatus().then(isLoggedIn => {
    if (!isLoggedIn) {
        document.querySelector('.login-button').style.display = 'block';
        document.querySelector('.signout-button').style.display = 'none';
    } else {
        document.querySelector('.login-button').style.display = 'none';
        document.querySelector('.signout-button').style.display = 'block';
    }
});

