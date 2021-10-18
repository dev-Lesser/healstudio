import axios from "axios"

const BASE_URL = "http://localhost:8000"

export const get_boards = async (skip) => {
    const url = `${BASE_URL}/boards`
    const result = await axios.get(url, {params: {
        skip: skip
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}

export const get_board = async (id, user, skip, limit) => {
    const url = `${BASE_URL}/board/${id}`
    const result = await axios.get(url, {params: {
        user: user,
        skip: skip,
        limit: limit
    }})
    if (result.status == 200) {
        return [true, result.data]
    }
    return [false, null]
}