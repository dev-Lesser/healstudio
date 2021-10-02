import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const get_region_list = async () => {
    const url = `${BASE_URL}/regions`
    const result = await axios.get(url, {})
    if (result.status == 200) {
        const data = result.data
        const values = Object.values(data)
        const regionlist = values.reduce((acc, curr) => acc.concat(curr), [])
        return [true, regionlist]
    }
    return [false, null]
}


export const get_gyms_list = async (skip, limit) => {
    const url = `${BASE_URL}/gyms-lists`
    const result = await axios.get(url, {params: {
        skip: skip,
        limit: limit
    }})
    if (result.status == 200) {
        const data = result.data
        const values = Object.values(data)
        const gymList = values.reduce((acc, curr) => acc.concat(curr), [])
        return [true, gymList]
    }
    return [false, null]
}
