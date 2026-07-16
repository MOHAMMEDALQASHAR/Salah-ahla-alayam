let token = localStorage.getItem('admin_token');

// ترجمة حالات الحجز
const statusLabels = {
    'pending': 'قيد الانتظار',
    'confirmed': 'مؤكد',
    'cancelled': 'ملغي'
};

document.addEventListener('DOMContentLoaded', () => {
    if(token) {
        showDashboard();
    }

    const loginForm = document.getElementById('loginForm');
    if(loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);

                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData
                });

                if(response.ok) {
                    const data = await response.json();
                    token = data.access_token;
                    localStorage.setItem('admin_token', token);
                    showDashboard();
                } else {
                    const msg = document.getElementById('loginMessage');
                    msg.className = 'message error';
                    msg.textContent = 'اسم المستخدم أو كلمة المرور غير صحيحة';
                }
            } catch (error) {
                console.error('Login error:', error);
            }
        });
    }

    // Upload form
    const uploadForm = document.getElementById('uploadForm');
    if(uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('imageFile');
            if(fileInput.files.length === 0) return;

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            try {
                const response = await fetch('/images/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData
                });
                
                if(response.ok) {
                    uploadForm.reset();
                    loadAdminGallery();
                }
            } catch (error) {
                console.error('Upload error:', error);
            }
        });
    }

    // Settings form
    const settingsForm = document.getElementById('settingsForm');
    if(settingsForm) {
        settingsForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const price = document.getElementById('setDailyPrice').value;
            const phone = document.getElementById('setContactPhone').value;

            try {
                await fetch('/settings/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ key: 'daily_price', value: price })
                });

                await fetch('/settings/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ key: 'contact_phone', value: phone })
                });

                const msg = document.getElementById('settingsMessage');
                msg.className = 'message success';
                msg.textContent = 'تم حفظ الإعدادات بنجاح';
            } catch (error) {
                console.error('Error saving settings:', error);
            }
        });
    }
});

function showDashboard() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('dashboardSection').style.display = 'flex';
    loadBookings();
}

function logout() {
    localStorage.removeItem('admin_token');
    token = null;
    document.getElementById('loginSection').style.display = 'flex';
    document.getElementById('dashboardSection').style.display = 'none';
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.querySelectorAll('.sidebar-menu a').forEach(a => a.classList.remove('active'));
    
    document.getElementById(`tab-${tabName}`).style.display = 'block';
    event.target.classList.add('active');

    if(tabName === 'bookings') loadBookings();
    if(tabName === 'gallery') loadAdminGallery();
    if(tabName === 'settings') loadAdminSettings();
}

async function loadBookings() {
    try {
        const response = await fetch('/bookings/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(response.status === 401) return logout();

        const bookings = await response.json();
        const tbody = document.querySelector('#bookingsTable tbody');
        tbody.innerHTML = '';

        if (bookings.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 40px;">لا توجد حجوزات حالياً</td></tr>';
            return;
        }

        bookings.forEach(b => {
            const statusText = statusLabels[b.status] || b.status;
            const idCard = b.id_card_number || '—';
            const eventType = b.event_type || '—';
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${b.date}</td>
                <td>${b.customer_name}</td>
                <td dir="ltr" style="text-align: right;">${b.contact_phone}</td>
                <td>${idCard}</td>
                <td>${eventType}</td>
                <td><span class="status-badge status-${b.status}">${statusText}</span></td>
                <td>
                    <button class="action-btn" onclick="updateStatus(${b.id}, 'confirmed')" title="تأكيد">✅ تأكيد</button>
                    <button class="action-btn" onclick="updateStatus(${b.id}, 'cancelled')" title="إلغاء">❌ إلغاء</button>
                    <button class="action-btn" onclick="deleteBooking(${b.id})" style="color: var(--error)" title="حذف">🗑 حذف</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

async function updateStatus(id, status) {
    try {
        await fetch(`/bookings/${id}/status?status=${status}`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadBookings();
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

async function deleteBooking(id) {
    if(!confirm('هل أنت متأكد من حذف هذا الحجز؟')) return;
    try {
        await fetch(`/bookings/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadBookings();
    } catch (error) {
        console.error('Error deleting booking:', error);
    }
}

async function loadAdminGallery() {
    try {
        const response = await fetch('/images/');
        const images = await response.json();
        const container = document.getElementById('adminGallery');
        container.innerHTML = '';

        if (images.length === 0) {
            container.innerHTML = '<p style="color: var(--text-muted); text-align: center; grid-column: 1/-1; padding: 40px;">لا توجد صور مرفوعة بعد</p>';
            return;
        }

        images.forEach(img => {
            const div = document.createElement('div');
            div.className = 'gallery-item';
            div.innerHTML = `
                <img src="/uploads/${img.filename}" alt="${img.filename}">
                <button class="delete-btn" onclick="deleteImage(${img.id})">🗑 حذف</button>
            `;
            container.appendChild(div);
        });
    } catch (error) {
        console.error('Error loading admin gallery:', error);
    }
}

async function deleteImage(id) {
    if(!confirm('هل أنت متأكد من حذف هذه الصورة؟')) return;
    try {
        await fetch(`/images/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadAdminGallery();
    } catch (error) {
        console.error('Error deleting image:', error);
    }
}

async function loadAdminSettings() {
    try {
        const response = await fetch('/settings/');
        const data = await response.json();
        
        data.forEach(setting => {
            if(setting.key === 'daily_price') {
                document.getElementById('setDailyPrice').value = setting.value;
            } else if(setting.key === 'contact_phone') {
                document.getElementById('setContactPhone').value = setting.value;
            }
        });
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}
