# Function used to convert our time strings to minutes, to make calculations easier.
def convert_to_minutes(time_str):
    """Convert a time string (HH:MM) to minutes since midnight."""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

# Function used to convert our minutes back to time strings, so they print properly.
def convert_to_time_string(minutes):
    """Convert minutes since midnight back to a time string (HH:MM)."""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

def find_available_slots(person1_schedule, person1_working, person2_schedule, person2_working, duration):
    # Convert working periods to minutes using convert_to_minutes function.
    p1_work_start = convert_to_minutes(person1_working[0])
    p1_work_end = convert_to_minutes(person1_working[1])
    p2_work_start = convert_to_minutes(person2_working[0])
    p2_work_end = convert_to_minutes(person2_working[1])

    # Collect all busy times for both workers.
    busy_times = []
    for schedule in [person1_schedule, person2_schedule]:
        for start, end in schedule:
            busy_times.append((convert_to_minutes(start), convert_to_minutes(end)))
    busy_times.sort()

    # Test for any overlap in busy times, and remove them if necessary.
    merged_busy = []
    for start, end in busy_times:
        if not merged_busy or merged_busy[-1][1] < start:
            merged_busy.append((start, end))
        else:
            merged_busy[-1] = (merged_busy[-1][0], max(merged_busy[-1][1], end))

    # Collect all free times for both workers.
    free_slots = []
    current_start = max(p1_work_start, p2_work_start)

    for start, end in merged_busy:
        if current_start < start:  # Free slot exists
            free_end = min(start, min(p1_work_end, p2_work_end))
            if free_end - current_start >= duration:
                meeting_end = current_start + duration
                if meeting_end < free_end:
                    # Append the first time that the meeting can start, and the latest it can run too.
                    free_slots.append((current_start, free_end))
        current_start = max(current_start, end)

    # Test case for any free slots after the busy times.
    if current_start < min(p1_work_end, p2_work_end):
        free_end = min(p1_work_end, p2_work_end)
        meeting_end = current_start + duration
        if meeting_end <= free_end:
            free_slots.append((current_start, meeting_end))

    # Convert free slots back to time strings 
    available_slots = []
    for start, end in free_slots:
        available_slots.append([convert_to_time_string(start), convert_to_time_string(end)])

    return available_slots

def execute_test_cases():
    print("Running test cases...\n")
    
    print("\n\nTest Case #1 Basic case with partial overlapping schedules...")
    print(find_available_slots(
        [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']],
        ['9:00', '19:00'],
        [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']],
        ['9:00', '18:30'],
        30
    ))

    print("\n\nTest Case #2: No overlapping work hours...")
    print(find_available_slots(
        [['10:00', '11:00']],
        ['9:00', '12:00'],
        [['13:00', '14:00']],
        ['13:00', '18:00'],
        30
    ))

    print("\n\nTest Case #3 (Edge Case): Both individuals are occupied during work hours...")
    print(find_available_slots(
        [['9:00', '18:00']],
        ['9:00', '18:00'],
        [['9:00', '18:00']],
        ['9:00', '18:00'],
        30
    ))

    print("\n\nTest Case #4 (Edge Case): Duration of the meeting is longer than any of the available slots...")
    print(find_available_slots(
        [['9:30', '10:00'], ['14:00', '15:00']],
        ['9:00', '17:00'],
        [['11:00', '11:30'], ['15:30', '16:00']],
        ['9:00', '17:00'],
        120
    ))

    print("\n\nTest Case #5: One of the individuals has no schedule / no working hours...")
    print(find_available_slots(
        [],
        ['9:00', '17:00'],
        [['10:00', '11:00'], ['13:00', '14:00']],
        ['9:00', '17:00'],
        30
    ))

    print("\n\nTest Case #6: Case where the meeting duration is extremely short (only 3 minutes)...")
    print(find_available_slots(
        [['9:00', '9:05'], ['12:00', '13:00']],
        ['9:00', '17:00'],
        [['10:00', '10:05'], ['15:00', '15:05']],
        ['9:00', '17:00'],
        3
    ))

    print("\n\nTest Case #7: Short 15 minute meeting...")
    print(find_available_slots(
        [['9:00', '9:30'], ['11:00', '11:30'], ['14:00', '14:30']],
        ['9:00', '17:00'],
        [['10:00', '10:30'], ['12:00', '12:30'], ['15:00', '15:30']],
        ['9:00', '17:00'],
        15
    ))

    print("\n\nTest Case #8: Partial overlap between the working hours of both people...")
    print(find_available_slots(
        [['8:00', '9:30'], ['15:00', '16:00']],
        ['8:00', '16:00'],
        [['14:00', '15:00'], ['17:00', '18:00']],
        ['13:00', '18:00'],
        30
    ))

    print("\n\nTest Case #9: Large time gaps in both of the schedules...")
    print(find_available_slots(
        [['9:00', '10:00'], ['15:00', '16:00']],
        ['9:00', '18:00'],
        [['11:00', '12:00'], ['17:00', '18:00']],
        ['10:00', '19:00'],
        60
    ))

    print("\n\nTest Case #10: Both individuals entirely free during working hours...")
    print(find_available_slots(
        [],
        ['9:00', '17:00'],
        [],
        ['9:00', '17:00'],
        120
    ))

execute_test_cases()
