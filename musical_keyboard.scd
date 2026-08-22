s.boot;
(
SynthDef(\tecla, { |freq=440, amp=0.5, att=0.01, rel=0.8, wave=0|
    var sig, env;
    env = EnvGen.ar(Env.perc(att, rel), doneAction: 2);
    sig = Select.ar(wave, [
        SinOsc.ar(freq),
        Pulse.ar(freq),
        LFTri.ar(freq),
        Saw.ar(freq)
    ]) * amp * env;
    Out.ar(0, sig ! 2);
}).add;
)

(
OSCdef(\nota, { |msg|
    var freq = msg[1];
    var waveStr = msg[2];
    var amp = msg[3] ? 0.5;
    var waveIndex = ["sine", "square", "triangle", "saw"].indexOf(waveStr) ? 0;
    Synth(\tecla, [\freq, freq, \amp, amp, \wave, waveIndex]);
}, '/nota');
)