from ..util.PID import PID

pid = PID()
pid.SetPoint = 3
encoder_feedback = 20
duty = 40

while True:
    print('duty ', duty, encoder_feedback, pid.output)
    pid.update(encoder_feedback)
    duty += pid.output

    # Real world
    encoder_feedback = min(duty * .5, 50)

    r = input()
    if r.strip():
        pid.SetPoint = int(r)
