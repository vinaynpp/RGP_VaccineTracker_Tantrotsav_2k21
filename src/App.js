import './App.css'
import React, { useEffect, useState } from 'react'
import {
  COUNT_NAMESPACE,
  COUNT_KEY,
  fetchApiData,
  NUMBER_REGEX,
  PUBLIC_IMAGE_PATH,
  getDate
} from './utils/Constants'
import * as statesData from './JsonData/states.json'
import { borderRadius, primaryColor } from './utils/Theme'
import useInterval from './utils/useInterval'
import MaxWidthWrapper from './utils/MaxWidthWrapper'


function App () {
  const [isMobile, setIsMobile] = useState(false)

  // Toggle between pincode and district search
  const [toggleValue, setToggleValue] = useState('pincode')
  const [searchMode, setSearchMode] = useState('pincode')

  // Starts to fetch from api only if pincode entered is valid || district is selected.
  const [apiFetching, setApiFetching] = useState(false)

  // Input values
  const [input, setInput] = useState('')
  const [inputError, setInputError] = useState(false)
  //pincodes value when search btn clicked
  const [searchQuery, setSearchQuery] = useState('')

  // District array
  const [districts, setDistricts] = useState([])
  const [selectedDistrict, setSelectedDistrict] = useState('')
  const [selectBoxError, setSelectBoxError] = useState({
    state: false,
    district: false
  })

  const [showToast, setShowToast] = useState({
    status: false,
    message: { head: '', content: '' }
  })

  return (
    <div className='App'>
      <div className='backgroundCircle'> </div>{' '}
      <MaxWidthWrapper>
        <div className='contentContainers'>
          <div className='leftContainer'>
            <img
              src={PUBLIC_IMAGE_PATH + 'logo-title.png'}
              className='brandLogo'
              alt='RPG VACCINE TRACKER'
            />
            <h1 className='mainHead'>
              Get notified when your area has available slots{' '}
            </h1>
            <ToggleSlider setSearchMode={value => handleToggle(value)} />
            {toggleValue === 'pincode' && (
              // PINCODE SEARCH
              <div
                className='inputContainer'
                style={{
                  border: inputError && `1px solid red`,
                  borderRadius: borderRadius
                }}
              >
                <input
                  placeholder='Enter your Pincode'
                  type='text'
                  className='input'
                  value={input}
                  onChange={e => {
                    handleInput(e.target.value)
                  }}
                  maxLength={6}
                />
                <img
                  src={PUBLIC_IMAGE_PATH + 'search.svg'}
                  className='searchIcon'
                  alt=''
                  width={22}
                  height={23}
                />{' '}
              </div>
            )}
            {toggleValue === 'district' && (
              // DISTRICT SEARCH
              <div className='selectBoxContainer'>
                <SelectBox
                  title='Select State'
                  array={statesData.states}
                  idValue={'state_id'}
                  labelValue={'state_name'}
                  error={selectBoxError.state}
                  executeFunction={value => {
                    getDistricts(value)
                  }}
                />
                <SelectBox
                  title='Select District'
                  array={districts.districts}
                  idValue={'district_id'}
                  labelValue={'district_name'}
                  error={selectBoxError.district}
                  executeFunction={value => {
                    handleDistrictChange(value)
                  }}
                />{' '}
              </div>
            )}
            <div className='checklistContainer'>
              <div className='checklistTop'>
                <Checkbox
                  text='18-44'
                  checked={true}
                  value={18}
                  executeFunction={value =>
                    handleCheckboxFilterModes('age', value)
                  }
                />{' '}
                <Checkbox
                  text='45+'
                  value={45}
                  executeFunction={value =>
                    handleCheckboxFilterModes('age', value)
                  }
                />
                <Checkbox
                  text='Free'
                  value={'Free'}
                  executeFunction={value =>
                    handleCheckboxFilterModes('fee', value)
                  }
                />{' '}
                <Checkbox
                  text='Paid'
                  value='Paid'
                  executeFunction={value =>
                    handleCheckboxFilterModes('fee', value)
                  }
                />{' '}
              </div>
              <div className='checklistBottom'>
                <Checkbox
                  text='Covaxin'
                  value='COVAXIN'
                  executeFunction={value =>
                    handleCheckboxFilterModes('vaccine', value)
                  }
                />{' '}
                <Checkbox
                  text='Covishield'
                  value='COVISHIELD'
                  executeFunction={value =>
                    handleCheckboxFilterModes('vaccine', value)
                  }
                />{' '}
                <Checkbox
                  text='Sputnik V'
                  value='SPUTNIK V'
                  executeFunction={value =>
                    handleCheckboxFilterModes('vaccine', value)
                  }
                />{' '}
              </div>{' '}
            </div>
            <div className='btnContainer'>
              <span className='btnFrame'>
                <Button
                  text='Need Help?'
                  background={'#fff'}
                  color={primaryColor}
                  borderRadius={borderRadius}
                  onClick={() => setShowModal(true)}
                />{' '}
              </span>
              <span className='btnFrame'>
                <Button
                  text='Get Notified'
                  borderRadius={borderRadius}
                  animate={
                    (input.length === 6 && true) ||
                    (selectedDistrict.length && true)
                  }
                  onClick={() => {
                    handleSearch()
                  }}
                />{' '}
              </span>
              <Modal
                show={showModal}
                close={() => setShowModal(false)}
                title='Need Help?'
                children={<HelpModal />}
              />{' '}
            </div>{' '}
          </div>
          <div className='rightContainer' id='rightContainer'>
            <div className='slotsContainer'>
              <h4> SLOTS AVAILABLE </h4>{' '}
              <div className='slotsContainerScrollbar'>
                {' '}
                {filteredData.length > 0 ? (
                  filteredData.map((center, index) => (
                    <div className='slotCard' key={index}>
                      <SlotCard data={center} />{' '}
                    </div>
                  ))
                ) : (
                  <div
                    className='slotsNotFoundContainer'
                    style={{ display: !apiFetching && 'none' }}
                  >
                    <span>
                      No slots available according to your filters <br /> We
                      will notify you as soon as a vacant slot appears!
                    </span>{' '}
                    <div className='loader-cont'>
                      <Loader />
                    </div>{' '}
                  </div>
                )}{' '}
              </div>{' '}
            </div>{' '}
            <div className='registerContainer'>
              <h3 className='registerContainer-head'> Register through </h3>{' '}
              <a
                href='https://play.google.com/store/apps/details?id=nic.goi.aarogyasetu&hl=en_IN&gl=US'
                target='blank'
              >
                <img
                  src={PUBLIC_IMAGE_PATH + 'arogya.png'}
                  className='registerContainer-img'
                  alt=''
                />
              </a>{' '}
              <a href='https://web.umang.gov.in/landing/' target='blank'>
                <img
                  src={PUBLIC_IMAGE_PATH + 'umang.png'}
                  className='registerContainer-img'
                  alt=''
                />
              </a>{' '}
              <a href='https://www.cowin.gov.in/home' target='blank'>
                <img
                  src={PUBLIC_IMAGE_PATH + 'cowin.png'}
                  className='registerContainer-img'
                  alt=''
                />
              </a>{' '}
            </div>{' '}
          </div>{' '}
        </div>
        {showToast.status && (
          <Toast
            heading={showToast.message.head}
            content={showToast.message.content}
            resetToast={() =>
              setShowToast({
                status: false,
                message: { head: '', content: '' }
              })
            }
          />
        )}{' '}
      </MaxWidthWrapper>
      <Footer />
    </div>
  )
}

export default App
