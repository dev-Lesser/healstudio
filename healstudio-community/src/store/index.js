import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

var today = new Date();
var dd = String(today.getDate()).padStart(2, "0");
var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
var yyyy = today.getFullYear();
var date = yyyy + "-" + mm + "-" + dd;

var pdd = '01'
var pyyyy = yyyy
var pmm = String(today.getMonth()).padStart(2, "0");
if (mm == '01') {
    pyyyy -= 1
    pmm = '12'
}
var pdate = pyyyy + '-' + pmm + '-' + pdd

export default new Vuex.Store({
    state: {
        brand: null,
        startDate: pdate,
        endDate: date,
        lastSearch: null,
        branlistLog: null,
        brandShare: null,
        brandFreq: null,
        brandBubble: null,
        brandCooccur: null,
        brandUser: null,
        brandIndex: null,
        brandList: null,
        productsShare: null,
        productsReview: null,

    },
    getters: {
        getBrand: state => state.brand,
        getDate: state => [state.startDate, state.endDate],
        getBrandDate: state => [state.brand, state.startDate, state.endDate],
        getLastSearchKey: state => state.lastSearch,
        getAlreadySearch: state => (state.lastSearch === state.brand + state.startDate + state.endDate),
        alreadyLoadBrandList: state => (state.branlistLog === state.startDate + state.endDate),
        getBrandList: state => state.brandList,

        getBrandShareData: state => state.brandShare,
        getBrandReviewData: state => [state.brandFreq, state.brandBubble, state.brandCooccur],
        getBrandUserData: state => state.brandUser,
        getBrandIndexData: state => state.brandIndex,

        getPShareData: state => state.productsShare,
        getPReviewData: state => state.productsReview,
    },
    mutations: {
        set_brand_list: (state, list) => {
            state.brandList = list
            state.branlistLog = state.startDate + state.endDate
        },
        change_start_date: (state, newDate) => (state.startDate = newDate),
        change_end_date: (state, newDate) => (state.endDate = newDate),
        change_brand: (state, newBrand) => state.brand = newBrand,
        set_search_info: (state) => state.lastSearch = state.brand + state.startDate + state.endDate,

        set_brand_share: (state, newData) => state.brandShare = newData,

        set_brand_freq: (state, newData) => state.brandFreq = newData,
        set_brand_bubble: (state, newData) => state.brandBubble = newData,
        set_brand_cooccur: (state, newData) => state.brandCooccur = newData,

        set_brand_user: (state, newData) => state.brandUser = newData,
        set_brand_index: (state, newData) => state.brandIndex = newData,

        set_products_share: (state, newData) => state.productsShare = newData,
        set_products_review: (state, newData) => state.productsReview = newData,

        reset_data: (state) => {
            state.brandShare = null
            state.brandFreq = null
            state.brandBubble = null
            state.brandCooccur = null
            state.brandUser = null
            state.brandIndex = null
            state.productsShare = null
            state.productsReview = null
            state.lastSearch = null
        }
    },
    actions: {},
    modules: {}
})