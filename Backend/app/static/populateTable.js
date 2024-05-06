document.addEventListener('DOMContentLoaded', function() {

    let scheduleInputs = document.getElementById("scheduleInputs");

    for (let i = 0; i < 7; i++) {
        let dayName = new Date();
        dayName.setDate(dayName.getDate() + i);
        dayName = dayName.toLocaleDateString('en-AU', { weekday: 'long' });

        let inputDiv = document.createElement("div");
        inputDiv.classList.add("day-inputs");
        inputDiv.innerHTML = `
            <h3>${dayName}</h3>
            <label for="start_${i}">Start Time:</label>
            <input type="time" id="start_${i}">
            <br>
            <label for="end_${i}">End Time:</label>
            <input type="time" id="end_${i}">
            <br>
        `;
        scheduleInputs.appendChild(inputDiv);
    }
    // Get references to calendar elements
    const calendarContainer = document.querySelector('.calendar');
    const dateCells = calendarContainer.querySelectorAll('.headcol:not(.past), .today, .secondary'); // Select non-past headers and weekdays
    const eventContainer = calendarContainer.querySelector('.wrap'); // Container for event elements
  
    // Function to update the calendar dates (assuming you have logic to dynamically set dates)

    function getNthTableCell(tableSelector, rowIndex, colIndex) {
        const table = document.querySelector(tableSelector); // Replace with your table's selector

        if (table) {
            const row = table.querySelector(`tr:nth-child(${rowIndex})`);
            if (row) {
            const nthCell = row.querySelector(`td:nth-child(${colIndex})`);
            if (nthCell) {
                return nthCell;
            } else {
                console.log(`${colIndex}th cell in ${rowIndex}th row not found.`);
            }
            } else {
            console.log(`${rowIndex}th table row not found.`);
            }
        } else {
            console.error("Table element not found.");
        }

        return null; // Indicate no cell found, row not found, or table not found
    }
  
    // Function to create a new event
    function createNewEvent(title, startTime, duration, dayIndex, pos) {
      const eventElement = document.createElement('div');
      eventElement.classList.add('event');
      eventElement.textContent = title;
      eventElement.style.cssText = 'height:200%;';
  
      // Calculate event position based on start time and duration
      const startHour = startTime.split(':')[0]; // Get hour from time string
      const startMinute = parseInt(startTime.split(':')[1]); // Get minutes from time string
      const appendHour = startHour * 4 + parseInt(startMinute / 15) + 1;

      const appendDiv = getNthTableCell('.offset', appendHour, dayIndex); // Select 5th child element (tr)

      appendDiv.style.cssText = 'grid-template-columns: 1fr 1fr 1fr 1fr 1fr';
      eventElement.style.cssText = 'grid-column: ' + pos;

      alert(appendHour);
  
      const eventTop = (startHour * 60 + startMinute) * 2 + 'px'; // 2px per minute
      eventElement.style.top = eventTop;
  
      // Check if day cell exists (avoid errors for invalid dayIndex)
      if (dayIndex >= 0 && dayIndex < dateCells.length) {
        appendDiv.appendChild(eventElement);
      } else {
        alert("Invalid day index for new event.");
      }
    }
  
    // Function to handle event checkbox clicks (optional)
    function handleEventCheckboxClick(checkbox) {
      // Add functionality to handle checkbox clicks (e.g., display event details)
      console.log("Event checkbox clicked:", checkbox.nextElementSibling.textContent);  // Access event details
    }
  
  
    const eventCheckboxes = calendarContainer.querySelectorAll('.event .checkbox');
    eventCheckboxes.forEach(checkbox => {
      checkbox.addEventListener('click', () => handleEventCheckboxClick(checkbox));
    });
  
    // Example usage: Create new events (modify as needed)
    createNewEvent("Meeting", "09:00", 1, 5, 1); // Thursday, 9:00 AM for 1 hour
    createNewEvent("Lunch Break", "12:30", 0.5, 3, 1); // Saturday, 12:30 PM for 30 minutes
    createNewEvent("Lunch Break", "12:30", 0.5, 3, 2); // Saturday, 12:30 PM for 30 minutes
  });