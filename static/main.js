// Mark Attendance Function using Fetch API
function markAttendance() {
    const btn = document.getElementById('markAttendanceBtn');
    const messageDiv = document.getElementById('attendanceMessage');
    
    // Disable button and show loading
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Marking...';
    
    // Make AJAX request using Fetch API
    fetch('/student/mark_attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Success - show success message
            messageDiv.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="fas fa-check-circle"></i> ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Update statistics
            document.getElementById('totalDays').textContent = data.total_days;
            document.getElementById('totalPresent').textContent = data.total_present;
            document.getElementById('percentage').textContent = data.percentage + '%';
            
            // Add new row to attendance table
            const tableBody = document.querySelector('#attendanceTable tbody');
            if (tableBody) {
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>1</td>
                    <td>${data.date}</td>
                    <td>${data.time}</td>
                    <td>
                        <span class="badge bg-success">
                            <i class="fas fa-check"></i> Present
                        </span>
                    </td>
                `;
                tableBody.insertBefore(newRow, tableBody.firstChild);
                
                // Update row numbers
                updateRowNumbers();
            }
            
            // Change button to disabled state
            btn.innerHTML = '<i class="fas fa-check-circle"></i> Attendance Already Marked Today';
            btn.classList.remove('btn-success');
            btn.classList.add('btn-secondary');
            
        } else {
            // Error - show error message
            messageDiv.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-circle"></i> ${data.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            // Re-enable button
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-hand-paper"></i> Mark Attendance';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageDiv.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle"></i> An error occurred. Please try again.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Re-enable button
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-hand-paper"></i> Mark Attendance';
    });
}

// Update row numbers in table
function updateRowNumbers() {
    const rows = document.querySelectorAll('#attendanceTable tbody tr');
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});