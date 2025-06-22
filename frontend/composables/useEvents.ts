import type {Event} from '~/types/event'
import {createDirectus, readItems, rest} from '@directus/sdk'

export function useEvents() {
    const events: Ref<Event[] | null> = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchEvents = async () => {
        try {
            loading.value = true
            error.value = null

            const directus = createDirectus('http://localhost:8055').with(rest());
            events.value = await directus.request(readItems('date', {
                fields: [
                    "title", "start", "end", "venue", "notes", "group_id", "id"
                ],
                sort: ["start"],
                filter: {
                    _and: [
                        {
                            end: {
                                _gt: "$NOW"
                            }
                        }
                    ]
                }
            }))
        } catch (err: any) {
            error.value = err
            events.value = null
        } finally {
            loading.value = false
        }
    }

    onMounted(fetchEvents)

    return {
        events: events,
        loading,
        error,
        refresh: fetchEvents
    }
}


export function useSingleEvent(id: string | string[]) {
    const event: Ref<Event | null> = ref([])
    const loading = ref(true)
    const error = ref(null)

    const fetchEvent = async () => {
        try {
            loading.value = true
            error.value = null

            const directus = createDirectus('http://localhost:8055').with(rest());
            event.value = await directus.request(readItems('date', {
                fields: [
                    "title", "start", "end", "venue", "notes", "group_id", "id"
                ],
                filter: {
                    id: {
                        _eq: id
                    }
                }
            }))
        } catch (err: any) {
            error.value = err
            event.value = null
        } finally {
            loading.value = false
        }
    }

    onMounted(fetchEvent)

    return {
        event,
        loading,
        error,
        refresh: fetchEvent
    }
}