import json
from mingus.containers import Bar
from mingus.containers import Composition
from mingus.containers import Track
from counterpoint.lib.tracks import author
from counterpoint.lib.tracks import cantus_firmus
from counterpoint.lib.tracks import key
from counterpoint.lib.tracks import melodies
from counterpoint.lib.tracks import meter
from counterpoint.lib.structures import Alto
from counterpoint.lib.structures import Bass
from counterpoint.lib.structures import Soprano
from counterpoint.lib.structures import Tenor
from counterpoint.lib.species import first_species
from counterpoint.lib.species import fourth_species
from counterpoint.lib.species import second_species
from counterpoint.lib.species import third_species
from counterpoint.lib.errors import get_error_text
from counterpoint.lib.errors import written_rules
from counterpoint.lib.errors import standardize_errors

species = {
    'first': first_species,
    'second': second_species,
    'third': third_species,
    'fourth': fourth_species,
}
durations = {
    1: 'w',
    2: 'h',
    4: 'q',
    8: '8',
    16: '16',
    32: '32',
}

def mingus_to_vexflow(track):
    bars = []
    for bar in track:
        notes = []
        for note in bar:
            offset, duration, pitch = note
            duration_name = durations[duration]
            if pitch is None:
                pitch_name = 'b/4'
                duration_name += 'r'
            else:
                pitch_name = "%s/%d" % (pitch[0].name.lower(), pitch[0].octave)
            notes.append((pitch_name, duration_name))
        bars.append(notes)
    return bars

def view_exercise(context, request):
    # Create a composition, and add the vocal tracks to it.
    composition = Composition()
    composition.set_title('Counterpoint Exercise', '')
    composition.set_author(author, '')

    # Set up our vocal 'tracks' with the notes, key, meter defined in tracks.py
    tracks = {}
    for voice in [Soprano, Alto, Tenor, Bass]:
        if len(melodies[voice.name]):
            tracks[voice.name] = Track(instrument=voice())
            tracks[voice.name].add_bar(Bar(key=key, meter=meter))
            tracks[voice.name].name = voice.name
            for note in melodies[voice.name]:
                tracks[voice.name].add_notes(*note)
            composition.add_track(tracks[voice.name])

    errors = {}
    # Compute any errors.
    for s in species:
        error_dict = species[s](composition)
        errors[s] = [
            (get_error_text(e), written_rules.get(e[-1], ''))
            for e in standardize_errors(error_dict)
        ]

    notes = {}
    for track in composition.tracks:
        voice = track.name.lower()
        notes[voice] = mingus_to_vexflow(track)

    return dict(
        errors = errors,
        notes = json.dumps(notes),
    )
