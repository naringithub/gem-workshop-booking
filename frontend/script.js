/**
 * GEM Coupler Workshop - Booking System Frontend
 * Author: Manus AI
 * Date: October 4, 2025
 * Version: 1.0
 */

// Configuration
// Use relative URL so it works in both development and production
const API_BASE_URL = '/api';

// Global state
let selectedStation = null;
let selectedSlot = null;
let allStations = [];
let allTimeslots = [];

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    loadStations();
    setupEventListeners();
});

// ============================================================================
// LOAD STATIONS
// ============================================================================

async function loadStations() {
    try {
        const response = await fetch(`${API_BASE_URL}/stations`);
        const data = await response.json();
        
        if (data.success) {
            allStations = data.stations;
            renderStations(data.stations);
        } else {
            showError('ไม่สามารถโหลดข้อมูลสถานีได้');
        }
    } catch (error) {
        console.error('Error loading stations:', error);
        showError('เกิดข้อผิดพลาดในการเชื่อมต่อ');
    }
}

function renderStations(stations) {
    const container = document.getElementById('stations-grid');
    const loading = document.getElementById('loading');
    
    loading.style.display = 'none';
    container.innerHTML = '';
    
    stations.forEach(station => {
        const card = createStationCard(station);
        container.appendChild(card);
    });
}

function createStationCard(station) {
    const card = document.createElement('div');
    card.className = 'station-card';
    
    if (station.available === 0) {
        card.classList.add('full');
    }
    
    const icon = getStationIcon(station.id);
    const percentage = station.percentage || 0;
    
    card.innerHTML = `
        <div class="station-header">
            <div class="station-icon">${icon}</div>
            <div class="station-name">${station.name}</div>
        </div>
        
        <div class="station-info">
            <div class="info-row">
                <span>เวลา/คน:</span>
                <span>${station.time_per_person} นาที</span>
            </div>
            <div class="info-row">
                <span>ที่ว่าง:</span>
                <span>${station.available}/${station.total_capacity}</span>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${percentage}%"></div>
        </div>
        
        <button class="btn btn-primary" ${station.available === 0 ? 'disabled' : ''}>
            ${station.available === 0 ? 'เต็มแล้ว' : 'จองเลย'}
        </button>
    `;
    
    if (station.available > 0) {
        card.addEventListener('click', () => openBookingModal(station));
    }
    
    return card;
}

function getStationIcon(stationId) {
    const icons = {
        'gem': '🔹',
        'plate': '🦴',
        'leica': '🔬'
    };
    return icons[stationId] || '📋';
}

// ============================================================================
// MODAL MANAGEMENT
// ============================================================================

function setupEventListeners() {
    // Close modal
    document.querySelector('.close').addEventListener('click', closeModal);
    
    // Next to form
    document.getElementById('next-to-form').addEventListener('click', () => {
        showStep('step-form');
    });
    
    // Back to timeslot
    document.getElementById('back-to-timeslot').addEventListener('click', () => {
        showStep('step-timeslot');
    });
    
    // Submit form
    document.getElementById('booking-form').addEventListener('submit', handleBookingSubmit);
    
    // Back to home
    document.getElementById('back-to-home').addEventListener('click', () => {
        closeModal();
        location.reload();
    });
    
    // Download QR
    document.getElementById('download-qr').addEventListener('click', downloadQRCode);
}

function openBookingModal(station) {
    selectedStation = station;
    selectedSlot = null;
    
    document.getElementById('modal-title').textContent = `จอง ${station.name}`;
    document.getElementById('booking-modal').classList.add('show');
    
    showStep('step-timeslot');
    loadTimeslots(station.id);
}

function closeModal() {
    document.getElementById('booking-modal').classList.remove('show');
    selectedStation = null;
    selectedSlot = null;
}

function showStep(stepId) {
    document.querySelectorAll('.step').forEach(step => {
        step.style.display = 'none';
    });
    document.getElementById(stepId).style.display = 'block';
}

// ============================================================================
// TIMESLOTS
// ============================================================================

async function loadTimeslots(stationId) {
    try {
        const response = await fetch(`${API_BASE_URL}/timeslots?station=${stationId}`);
        const data = await response.json();
        
        if (data.success) {
            allTimeslots = data.timeslots;
            renderTimeslots(data.timeslots);
        } else {
            showError('ไม่สามารถโหลดช่วงเวลาได้');
        }
    } catch (error) {
        console.error('Error loading timeslots:', error);
        showError('เกิดข้อผิดพลาดในการเชื่อมต่อ');
    }
}

function renderTimeslots(timeslots) {
    const container = document.getElementById('timeslots-container');
    container.innerHTML = '';
    
    // Group by table
    const tables = {};
    timeslots.forEach(slot => {
        if (!tables[slot.table]) {
            tables[slot.table] = [];
        }
        tables[slot.table].push(slot);
    });
    
    // Render each table
    Object.keys(tables).sort().forEach(tableNum => {
        const tableGroup = document.createElement('div');
        tableGroup.className = 'table-group';
        
        const tableTitle = document.createElement('div');
        tableTitle.className = 'table-title';
        tableTitle.textContent = `โต๊ะ ${tableNum}`;
        tableGroup.appendChild(tableTitle);
        
        const slotsGrid = document.createElement('div');
        slotsGrid.className = 'timeslots-grid';
        
        tables[tableNum].forEach(slot => {
            const slotElement = createTimeslotElement(slot);
            slotsGrid.appendChild(slotElement);
        });
        
        tableGroup.appendChild(slotsGrid);
        container.appendChild(tableGroup);
    });
}

function createTimeslotElement(slot) {
    const element = document.createElement('div');
    element.className = 'timeslot';
    element.textContent = slot.time;
    
    if (!slot.available) {
        element.classList.add('unavailable');
    } else {
        element.addEventListener('click', () => selectTimeslot(slot, element));
    }
    
    return element;
}

function selectTimeslot(slot, element) {
    // Remove previous selection
    document.querySelectorAll('.timeslot.selected').forEach(el => {
        el.classList.remove('selected');
    });
    
    // Select new slot
    element.classList.add('selected');
    selectedSlot = slot;
    
    // Enable next button
    document.getElementById('next-to-form').disabled = false;
}

// ============================================================================
// BOOKING SUBMISSION
// ============================================================================

async function handleBookingSubmit(event) {
    event.preventDefault();
    
    if (!selectedSlot) {
        showError('กรุณาเลือกช่วงเวลา');
        return;
    }
    
    const formData = new FormData(event.target);
    const bookingData = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        institution: formData.get('institution'),
        position: formData.get('position'),
        station: selectedStation.id,
        slot_id: selectedSlot.slot_id
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/booking`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showConfirmation(data);
        } else {
            showError(data.error || 'ไม่สามารถจองได้');
        }
    } catch (error) {
        console.error('Error creating booking:', error);
        showError('เกิดข้อผิดพลาดในการเชื่อมต่อ');
    }
}

function showConfirmation(data) {
    // Show booking details
    const detailsContainer = document.getElementById('booking-details');
    detailsContainer.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Booking ID:</span>
            <span class="detail-value">${data.booking_id}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">สถานี:</span>
            <span class="detail-value">${data.details.station}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">เวลา:</span>
            <span class="detail-value">${data.details.time} น.</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">โต๊ะ:</span>
            <span class="detail-value">${data.details.table}</span>
        </div>
    `;
    
    // Show QR code
    document.getElementById('qr-code').src = data.details.qr_code;
    
    // Show confirmation step
    showStep('step-confirmation');
}

function downloadQRCode() {
    const qrCodeSrc = document.getElementById('qr-code').src;
    const link = document.createElement('a');
    link.href = qrCodeSrc;
    link.download = 'workshop-qr-code.png';
    link.click();
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function showError(message) {
    alert(message);
}

// Auto-refresh stations every 30 seconds
setInterval(() => {
    if (!document.getElementById('booking-modal').classList.contains('show')) {
        loadStations();
    }
}, 30000);
