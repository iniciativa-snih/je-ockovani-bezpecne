import stats from '/data/stats.json';
import submits from '/data/submits.json';
import vaccines from '/data/vaccines.json';
import date from 'date-and-time'

export const get = async (request) => {
    const s = stats[stats.length - 1]
    const v = vaccines[vaccines.length - 1]
    const d = Date.parse(submits.date_for)

    return {
        body: {
            date: d,
            stats: s,
            submits: submits.submits,
            vaccines: v
        }
    }
}
