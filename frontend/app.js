document.addEventListener('DOMContentLoaded', () => {
    // Load dynamic data
    loadSettings();
    loadGallery();

    // Force video play and handle sound
    const video = document.getElementById('heroVideo');
    const muteToggle = document.getElementById('muteToggle');
    const muteIcon = document.getElementById('muteIcon');
    const muteText = document.getElementById('muteText');

    if (video) {
        video.play().catch(error => console.log('Autoplay was prevented:', error));
        
        if (muteToggle) {
            muteToggle.addEventListener('click', () => {
                if (video.muted) {
                    video.muted = false;
                    muteIcon.className = 'fas fa-volume-up';
                    muteText.textContent = 'إيقاف الصوت';
                } else {
                    video.muted = true;
                    muteIcon.className = 'fas fa-volume-mute';
                    muteText.textContent = 'تشغيل الصوت';
                }
            });
        }
    }

    // Handle deposit box toggle
    const payDepositSelect = document.getElementById('pay_deposit');
    const depositInfoBox = document.getElementById('depositInfoBox');
    if (payDepositSelect && depositInfoBox) {
        payDepositSelect.addEventListener('change', (e) => {
            if (e.target.value === 'نعم') {
                depositInfoBox.style.display = 'block';
            } else {
                depositInfoBox.style.display = 'none';
            }
        });
    }

    const dateInput = document.getElementById('date');
    const bookingForm = document.getElementById('bookingForm');

    // Prevent past dates
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);

    // Check availability on date change
    dateInput.addEventListener('change', async (e) => {
        const date = e.target.value;
        if(!date) return;

        try {
            const response = await fetch(`/bookings/check/${date}`);
            const data = await response.json();
            
            const statusDiv = document.getElementById('availabilityStatus');
            const bookingFields = document.getElementById('bookingFields');
            const msgDiv = document.getElementById('bookingMessage');
            msgDiv.style.display = 'none';

            if(data.available) {
                statusDiv.innerHTML = '<span style="color: var(--success)">التاريخ متاح! يرجى إكمال بيانات الحجز.</span>';
                bookingFields.style.display = 'block';
            } else {
                statusDiv.innerHTML = `<span style="color: var(--error)">التاريخ غير متاح (${data.status})</span>`;
                bookingFields.style.display = 'none';
            }
        } catch (error) {
            console.error('Error checking availability:', error);
        }
    });

    // Handle form submission
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const date = document.getElementById('date').value;
        const name = document.getElementById('name').value;
        const phone = document.getElementById('phone').value;
        const id_card = document.getElementById('id_card').value;
        const event_type = document.getElementById('event_type').value;
        const pay_deposit = document.getElementById('pay_deposit').value;
        const receiptInput = document.getElementById('deposit_receipt');
        const receiptFile = receiptInput && receiptInput.files ? receiptInput.files[0] : null;
        
        try {
            let response;
            if (receiptFile) {
                const formData = new FormData();
                formData.append('date', date);
                formData.append('customer_name', name);
                formData.append('contact_phone', phone);
                formData.append('id_card_number', id_card);
                formData.append('event_type', event_type);
                formData.append('pay_deposit', pay_deposit);
                formData.append('receipt', receiptFile);

                response = await fetch('/bookings/with-receipt', {
                    method: 'POST',
                    body: formData
                });
            } else {
                response = await fetch('/bookings/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        date: date,
                        customer_name: name,
                        contact_phone: phone,
                        id_card_number: id_card,
                        event_type: event_type,
                        pay_deposit: pay_deposit,
                        deposit_receipt: ''
                    })
                });
            }

            const msgDiv = document.getElementById('bookingMessage');
            
            if(response.ok) {
                msgDiv.className = 'message success';
                msgDiv.style.display = 'block';
                msgDiv.textContent = 'تم إرسال طلب الحجز بنجاح! سنتواصل معك قريباً.';
                bookingForm.reset();
                if (depositInfoBox) depositInfoBox.style.display = 'none';
                document.getElementById('bookingFields').style.display = 'none';
                document.getElementById('availabilityStatus').innerHTML = '';
            } else {
                const data = await response.json();
                msgDiv.className = 'message error';
                msgDiv.style.display = 'block';
                let errorMsg = data.detail || 'حدث خطأ أثناء إرسال الطلب. يرجى المحاولة مرة أخرى.';
                if (Array.isArray(data.detail)) {
                    errorMsg = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
                }
                msgDiv.textContent = errorMsg;
            }
        } catch (error) {
            console.error('Error submitting booking:', error);
            const msgDiv = document.getElementById('bookingMessage');
            msgDiv.className = 'message error';
            msgDiv.style.display = 'block';
            msgDiv.textContent = 'حدث خطأ في الاتصال بالخادم. تأكد من تشغيل الباك اند.';
        }
    });
});

async function loadSettings() {
    try {
        const response = await fetch('/settings/');
        if (response.ok) {
            const data = await response.json();
            data.forEach(setting => {
                if(setting.key === 'daily_price') {
                    const el = document.getElementById('dailyPrice');
                    if (el) {
                        const num = Number(setting.value);
                        const formatted = !isNaN(num) && setting.value.trim() !== '' ? num.toLocaleString() : setting.value;
                        el.textContent = formatted + ' ريال يمني';
                    }
                } else if(setting.key === 'contact_phone') {
                    const el = document.getElementById('contactPhone');
                    if (el) el.textContent = setting.value;
                } else if(setting.key === 'bank_name') {
                    const el = document.getElementById('displayBankName');
                    if (el) el.textContent = setting.value;
                } else if(setting.key === 'bank_account_name') {
                    const el = document.getElementById('displayAccountName');
                    if (el) el.textContent = setting.value;
                } else if(setting.key === 'bank_account_number') {
                    const el = document.getElementById('displayAccountNumber');
                    if (el) el.textContent = setting.value;
                }
            });
        }
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

async function loadGallery() {
    const containerTop = document.getElementById('galleryContainerTop');
    const containerBottom = document.getElementById('galleryContainerBottom');
    if (!containerTop || !containerBottom) return;
    
    // Static images that are always shown
    const staticImagesTop = [
        '/static/images/1.jpeg',
        '/static/images/2.jpeg'
    ];
    
    const staticImagesBottom = [
        '/static/images/3.jpeg',
        '/static/images/4.jpeg'
    ];
    
    let allSourcesTop = [...staticImagesTop];
    let allSourcesBottom = [...staticImagesBottom];

    try {
        const response = await fetch('/images/');
        if (response.ok) {
            const images = await response.json();
            if (Array.isArray(images)) {
                images.forEach(img => {
                    const src = `/uploads/${img.filename}`;
                    if(img.row === 'bottom') {
                        allSourcesBottom.push(src);
                    } else {
                        // Default to top
                        allSourcesTop.push(src);
                    }
                });
            }
        }
    } catch (error) {
        console.warn('Error loading uploaded images from DB, using static gallery:', error);
    }
    
    // Build top marquee content (original + duplicate for infinite scroll)
    containerTop.innerHTML = '';
    for (let round = 0; round < 2; round++) {
        allSourcesTop.forEach((src, i) => {
            const div = document.createElement('div');
            div.className = 'gallery-item';
            div.innerHTML = `<img src="${src}" alt="صورة علوية ${i + 1}">`;
            containerTop.appendChild(div);
        });
    }

    // Build bottom marquee content (original + duplicate for infinite scroll)
    containerBottom.innerHTML = '';
    for (let round = 0; round < 2; round++) {
        allSourcesBottom.forEach((src, i) => {
            const div = document.createElement('div');
            div.className = 'gallery-item';
            div.innerHTML = `<img src="${src}" alt="صورة سفلية ${i + 1}">`;
            containerBottom.appendChild(div);
        });
    }

    // Adjust animation speed based on number of images
    const totalItemsTop = allSourcesTop.length;
    const speedTop = Math.max(20, totalItemsTop * 5);
    containerTop.style.animationDuration = speedTop + 's';

    const totalItemsBottom = allSourcesBottom.length;
    const speedBottom = Math.max(20, totalItemsBottom * 5);
    containerBottom.style.animationDuration = speedBottom + 's';
}
