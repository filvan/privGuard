from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.reports.common.tripsConfig import TripsConfig

class MotionProcessor:

    def __init__(self):
        pass

    @staticmethod
    def updateState(state, position, newState, tripsConfig):

        state.setEvent(None)

        oldState = state.getMotionState()
        if oldState == newState:
            if state.getMotionTime() is not None:
                oldTime = state.getMotionTime().getTime()
                newTime = position.getFixTime().getTime()

                distance = position.getDouble(Position.KEY_TOTAL_DISTANCE) - state.getMotionDistance()
                ignition = None
                if tripsConfig.getUseIgnition() and position.hasAttribute(Position.KEY_IGNITION):
                    ignition = position.getBoolean(Position.KEY_IGNITION)

                generateEvent = False
                if newState:
                    if newTime - oldTime >= tripsConfig.getMinimalTripDuration() or distance >= tripsConfig.getMinimalTripDistance():
                        generateEvent = True
                else:
                    if newTime - oldTime >= tripsConfig.getMinimalParkingDuration() or ignition is not None and not ignition:
                        generateEvent = True

                if generateEvent:

                    eventType = Event.TYPE_DEVICE_MOVING if newState else Event.TYPE_DEVICE_STOPPED
                    event = Event(eventType, position)

                    state.setMotionStreak(newState)
                    state.setMotionTime(None)
                    state.setMotionDistance(0)
                    state.setEvent(event)

        else:
            state.setMotionState(newState)
            if state.getMotionStreak() == newState:
                state.setMotionTime(None)
                state.setMotionDistance(0)
            else:
                state.setMotionTime(position.getFixTime())
                state.setMotionDistance(position.getDouble(Position.KEY_TOTAL_DISTANCE))
