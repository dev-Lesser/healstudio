import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const login = async (user_id, password) => {
    const body = { user_id, password }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: BASE_URL+'/login',
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    console.log(result)
    if (result.status == 201) {
        console.log('login success')
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
        // console.log(data)
        // const values = Object.values(data)
        // const gym = values.reduce((acc, curr) => acc.concat(curr), [])
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
        // console.log(data)
        // const values = Object.values(data)
        // const gym = values.reduce((acc, curr) => acc.concat(curr), [])
        return [true, data]
    }
    console.log(result)
    return [false, null]
}

export const get_reviews = async (gymId, skip, limit) => {
    const url = `${BASE_URL}/reviews/${gymId}`
    const result = await axios.get(url, {params: {
        
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
    console.log(result)
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
    console.log(result)
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