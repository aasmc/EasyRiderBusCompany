# Easy Rider Bus Company
Educational Project from JetBrains HyperSkill Academy. Python Core track. Level Challenging.

## Stage 1
### Description

You just started sorting out the existing database of the "Easy Rider" bus company. As you take the first look at the data, you realize that it's not going to be easy.

Sometimes numbers are missing from where they should definitely be. You also noticed that sometimes there are too many or too few characters. Fortunately, there is documentation to help you sort out this mess. However, this documentation is not a hundred percent complete: part of it was torn away when your colleague spilled coffee on it. Let's see what we can make out.

Here are the documents that you have: documentation and diagram of the bus lines.
### Objectives

- The string containing the data in JSON format is passed to standard input.
- Check that the data types match.
- Check that the required fields are filled in.
- Display the information about the number of found errors in total and in each field. Keep in mind that there might be no errors at all.
- The output should have the same formatting as shown in the example.

If you can't find the necessary information in the stage description, it can probably be found in the attached documentation.

Note that the type Char is present among the data types. 
### Examples
Input:

```json
[
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": 8.12
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "",
        "next_stop": 5,
        "stop_type": "",
        "a_time": "08:19"
    },
    {
        "bus_id": 128,
        "stop_id": 5,
        "stop_name": "Fifth Avenue",
        "next_stop": 7,
        "stop_type": "O",
        "a_time": "08:25"
    },
    {
        "bus_id": 128,
        "stop_id": "7",
        "stop_name": "Sesame Street",
        "next_stop": 0,
        "stop_type": "F",
        "a_time": "08:37"
    },
    {
        "bus_id": "",
        "stop_id": 2,
        "stop_name": "Pilotow Street",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": ""
    },
    {
        "bus_id": 256,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 6,
        "stop_type": "",
        "a_time": "09:45"
    },
    {
        "bus_id": 256,
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 7,
        "stop_type": "",
        "a_time": "09:59"
    },
    {
        "bus_id": 256,
        "stop_id": 7,
        "stop_name": "Sesame Street",
        "next_stop": "0",
        "stop_type": "F",
        "a_time": "10:12"
    },
    {
        "bus_id": 512,
        "stop_id": 4,
        "stop_name": "Bourbon Street",
        "next_stop": 6,
        "stop_type": "S",
        "a_time": "08:13"
    },
    {
        "bus_id": "512",
        "stop_id": 6,
        "stop_name": "Sunset Boulevard",
        "next_stop": 0,
        "stop_type": 5,
        "a_time": "08:16"
    }
]
```
Output:
```text
Type and required field validation: 8 errors
bus_id: 2
stop_id: 1
stop_name: 1
next_stop: 1
stop_type: 1
a_time: 2
```