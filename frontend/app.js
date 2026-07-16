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
        
        try {
            const response = await fetch('/bookings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    date: date,
                    customer_name: name,
                    contact_phone: phone,
                    id_card_number: id_card,
                    event_type: event_type
                })
            });

            const msgDiv = document.getElementById('bookingMessage');
            
            if(response.ok) {
                msgDiv.className = 'message success';
                msgDiv.style.display = 'block';
                msgDiv.textContent = 'تم إرسال طلب الحجز بنجاح! سنتواصل معك قريباً.';
                bookingForm.reset();
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
            msgDiv.textContent = 'حدث خطأ في الاتصال بالخادم. تأكد من تشغيل الباك اند على نفس المنفذ.';
        }
    });
});

async function loadSettings() {
    try {
        const response = await fetch('/settings/');
        const data = await response.json();
        
        data.forEach(setting => {
            if(setting.key === 'daily_price') {
                document.getElementById('dailyPrice').textContent = '$' + setting.value;
            } else if(setting.key === 'contact_phone') {
                document.getElementById('contactPhone').textContent = setting.value;
            }
        });
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

async function loadGallery() {
    try {
        const response = await fetch('/images/');
        const images = await response.json();
        const container = document.getElementById('galleryContainer');
        
        // Static images that are always shown
        const staticImages = [
            '/static/images/1.jpeg',
            '/static/images/2.jpeg',
            '/static/images/3.jpeg',
            '/static/images/4.jpeg'
        ];
        
        // Build all image sources: static + uploaded
        let allSources = [...staticImages];
        images.forEach(img => {
            allSources.push(`/uploads/${img.filename}`);
        });
        
        // Build marquee content (original + duplicate for infinite scroll)
        container.innerHTML = '';
        for (let round = 0; round < 2; round++) {
            allSources.forEach((src, i) => {
                const div = document.createElement('div');
                div.className = 'gallery-item';
                div.innerHTML = `<img src="${src}" alt="صورة ${i + 1}">`;
                container.appendChild(div);
            });
        }

        // Adjust animation speed based on number of images
        const totalItems = allSources.length;
        const speed = Math.max(20, totalItems * 5);
        container.style.animationDuration = speed + 's';
    } catch (error) {
        console.error('Error loading gallery:', error);
    }
}
