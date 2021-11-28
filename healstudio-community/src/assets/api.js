import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const get_meta = async () => {
    const url = `${BASE_URL}/metadata`
    const result = await axios.get(url, {})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

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

export const get_gym_by_id = async (id) => {
    const url = `${BASE_URL}/gym/${id}`
    const result = await axios.get(url)
    if (result.status == 200) {
        const data = result.data
        return [true, data]
    }
    return [false, null]
}

export const search_by_query = async (query, skip, limit) => {
    const url = `${BASE_URL}/search`
    const result = await axios.get(url, {params: {
        query: query,
        skip: skip,
        limit: limit
    }})
    if (result.status == 200) {
        const data = result.data
        return [true, data]
    }
    console.log(result)
    return [false, null]
}

export const get_reviews = async (gymId, skip, limit, user) => {
    const url = `${BASE_URL}/reviews/${gymId}`
    const result = await axios.get(url, {params: {
        skip: skip,
        limit: limit,
        user: user,
    }})
    if (result.status == 200) {
        const data = result.data
        return [true, data]
    }
    return [false, null]
}

export const get_trainers = async (gymId, skip, limit) => {
    const url = `${BASE_URL}/trainers/${gymId}`
    const result = await axios.get(url, {params: {
        skip: skip,
        limit: limit
    }})
    if (result.status == 200) {
        const data = result.data
        return [true, data]
    }
    return [false, null]
}

export const create_review = async (gymId, user_id, contents, point) => {
    const body = { user_id, contents, point }
    const url = `${BASE_URL}/review/${gymId}`
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 200) {
        console.log(`created ${gymId}`)
        return [true, result.data]
    }
    return [false, null]
}

export const update_review = async (id, gymId, user_id, contents, point) => {
    const body = { id, user_id, contents, point }
    const url = `${BASE_URL}/review/${gymId}`
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'patch',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 204) {
        console.log(`updated ${gymId}`)
        return [true, result.data]
    }
    return [false, null]
}

export const delete_review = async (id, gymId, user_id) => {
    const url = `${BASE_URL}/review/${gymId}?id=${id}&user_id=${user_id}`
    const result = await axios({
        method: 'delete',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
    })
    if (result.status == 200) {
        console.log(`deleted ${gymId}, ID: ${id}, USER_ID: ${user_id}, `)
        return [true, result.data]
    }
    return [false, null]
}

export const handle_favorite = async (user_id, gymId, uid) => {
    const body = { user_id, uid }
    var data = JSON.stringify(body);
    const url = `${BASE_URL}/favorite/${gymId}`
    const result = await axios({
        method: 'post',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 200) {
        // console.log(`deleted ${gymId}, ID: ${id}, USER_ID: ${user_id}, `)
        return [true, result.data]
    }
    return [false, null]
}

export const check_favorite = async (user_id, gymId, uid) => {
    const url = `${BASE_URL}/favorite/${gymId}?user_id=${user_id}&uid=${uid}`
    const result = await axios({
        method: 'get',
        url: url,
        headers: {
            'Content-Type': 'application/json'
        },
    })
    if (result.status == 200) {
        // console.log(`deleted ${gymId}, ID: ${id}, USER_ID: ${user_id}, `)
        return [true, result.data]
    }
    return [false, null]
}