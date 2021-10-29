import axios from "axios"

const BASE_URL = "http://localhost:8000"


export const login = async (user_id, password) => {
    const body = { user_id, password }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: `${BASE_URL}/auth/login`,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

export const signup = async (user_id, password) => {
    const body = { user_id, password }
    var data = JSON.stringify(body);
    const result = await axios({
        method: 'post',
        url: `${BASE_URL}/auth/signup`,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}
export const get_user_details = async (user_id, uuid) => {
    const url = `${BASE_URL}/user/${user_id}`
    const result = await axios.get(url, {params: {
        uid: uuid
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

