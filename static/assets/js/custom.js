    function formatDateToCustomString(date) {
        const months = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ];
        const parts = date.split('-');
        const day = parts[2];
        const month = months[parseInt(parts[1]) - 1];
        const year = parts[0];
        return `${day}/${month}/${year}`;
    }

    function populateTimeOptions(selectedDate) {
        // Get the current time in hours and minutes (24-hour format)
        const currentTime = new Date();
        const currentYear = currentTime.getFullYear();
        const currentMonth = currentTime.getMonth();
        const currentDay = currentTime.getDate();
        const currentHours = currentTime.getHours();
        const currentMinutes = currentTime.getMinutes();

        // Get the selected date and time
        const selectedDateObj = new Date(selectedDate);
        const selectedYear = selectedDateObj.getFullYear();
        const selectedMonth = selectedDateObj.getMonth();
        const selectedDay = selectedDateObj.getDate();

        // Calculate the minimum time for the time select dropdown
        let next30MinuteIntervalHours = currentHours;
        let next30MinuteIntervalMinutes = Math.ceil(currentMinutes / 30) * 30;
        if (next30MinuteIntervalMinutes === 60) {
            next30MinuteIntervalHours += 1;
            next30MinuteIntervalMinutes = 0;
        }

        // Clear previous time options
        const timeInput = document.getElementById('time_input');
        timeInput.innerHTML = '<option value="">Select time</option>';

   // If the selected date is in the future or today, add future time options only
    if (selectedYear > currentYear || selectedMonth > currentMonth || selectedDay > currentDay) {
        for (let h = 0; h < 24; h++) {
            for (let m = 0; m < 60; m += 30) {
                // Convert to 12-hour format with AM/PM designation
                const hour12Format = (h % 12 === 0) ? 12 : h % 12;
                const period = h < 12 ? 'AM' : 'PM';

                const optionText = `${hour12Format.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')} ${period}`;
                const optionValue = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
                const option = document.createElement('option');
                option.textContent = optionText;
                option.value = optionValue;
                timeInput.appendChild(option);
            }
        }
    } else { // If the selected date is today or in the past, add future time options from the current time
        for (let h = next30MinuteIntervalHours; h < 24; h++) {
            for (let m = (h === next30MinuteIntervalHours ? next30MinuteIntervalMinutes : 0); m < 60; m += 30) {
                // Convert to 12-hour format with AM/PM designation
                const hour12Format = (h % 12 === 0) ? 12 : h % 12;
                const period = h < 12 ? 'AM' : 'PM';

                const optionText = `${hour12Format.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')} ${period}`;
                const optionValue = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
                const option = document.createElement('option');
                option.textContent = optionText;
                option.value = optionValue;
                timeInput.appendChild(option);
            }
        }
    }
}

    // Set the default date to today with the custom format "28/Jul/2023"
    const dateInput = document.getElementById('date_input');
    const currentDate = new Date();
    const formattedDate = formatDateToCustomString(currentDate.toISOString().split('T')[0]);
    dateInput.value = formattedDate;
    populateTimeOptions(dateInput.value);


    // Populate the time options when the date input changes
    dateInput.addEventListener('change', function() {
        const selectedDate = dateInput.value;
        populateTimeOptions(selectedDate);
    });

    // Set the default date to today when the time input gains focus
    const timeInput = document.getElementById('time_input');
    timeInput.addEventListener('focus', function() {
        if (!dateInput.value) {
            const formattedDate = formatDateToCustomString(currentDate.toISOString().split('T')[0]);
            dateInput.value = formattedDate;
            populateTimeOptions(dateInput.value);
        }
    });

    // Show the time list when the time select dropdown is clicked

    // Show the time list when the time select dropdown is clicked
timeInput.addEventListener('click', function() {
    const timeList = document.getElementById('time_list');
    if (timeList) {
        if (timeList.style.display === 'none') {
            timeList.innerHTML = '';
            for (const option of timeInput.options) {
                if (option.value) {
                    const timeOption = document.createElement('li');
                    timeOption.textContent = option.textContent;
                    timeList.appendChild(timeOption);
                }
            }
            timeList.style.display = 'block';
        } else {
            timeList.style.display = 'none';
        }
    }
});

// Set the selected time from the time list to the select dropdown
if (timeList) {
    timeList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            timeInput.value = event.target.textContent;
            timeList.style.display = 'none';
        }
    });
}




