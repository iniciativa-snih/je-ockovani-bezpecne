import stats from '/data/stats.json';
import submits from '/data/submits.json';
import vaccines from '/data/vaccines.json';
import date from 'date-and-time'

s = stats.pop();
v = vaccines.pop();
d = Date.parse(submits.date_for);

export const get = async (request) => {

    return {
        body: {
            date: d,
            stats: s,
            submits: submits.submits,
            vaccines: v
        }
    }
}
