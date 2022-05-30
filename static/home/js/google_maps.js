"use strict";

function initMap() {
  const CONFIGURATION = {
    "ctaTitle": "Checkout",
    "mapOptions": {"center":{"lat":31.2533973,"lng":34.7893771},"fullscreenControl":true,"mapTypeControl":false,"streetViewControl":true,"zoom":11,"zoomControl":true,"maxZoom":22},
    "mapsApiKey": "AIzaSyD8UkSs_yEEw3SgfYVTe1Gkdxz2pnu-ju0",
    "capabilities": {"addressAutocompleteControl":true,"mapDisplayControl":true,"ctaControl":true}
  };
  const componentForm = [
    'location',
    'locality',
    'administrative_area_level_1',
    'country',
    'postal_code',
  ];
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: CONFIGURATION.mapOptions.zoom,
    center: { lat: 31.2533973, lng: 34.7893771 },
    mapTypeControl: false,
    fullscreenControl: CONFIGURATION.mapOptions.fullscreenControl,
    zoomControl: CONFIGURATION.mapOptions.zoomControl,
    streetViewControl: CONFIGURATION.mapOptions.streetViewControl
  });
  const marker = new google.maps.Marker({map: map, draggable: false});
  const autocompleteInput = document.getElementById('location');
  const autocomplete = new google.maps.places.Autocomplete(autocompleteInput, {
    fields: ["address_components", "geometry", "name"],
    types: ["address"],
  });
  autocomplete.addListener('place_changed', function () {
    marker.setVisible(false);
    const place = autocomplete.getPlace();
    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert('No details available for input: \'' + place.name + '\'');
      return;
    }
    renderAddress(place);
    fillInAddress(place,lat,lng);
  });

  function fillInAddress(place,lat,lng) {  // optional parameter
    const addressNameFormat = {
      'street_number': 'short_name',
      'route': 'long_name',
      'locality': 'long_name',
      'administrative_area_level_1': 'short_name',
      'country': 'long_name',
      'postal_code': 'short_name',
    };
    const getAddressComp = function (type) {
      for (const component of place.address_components) {
        if (component.types[0] === type) {
          return component[addressNameFormat[type]];
        }
      }
      return '';
    };
    document.getElementById('location').value = getAddressComp('street_number') + ' '
              + getAddressComp('route');
    for (const component of componentForm) {
      // Location field is handled separately above as it has different logic.
      if (component !== 'location' && component !== 'latitude' && component !== 'longitude') {
        document.getElementById(component).value = getAddressComp(component);
      }
    }
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;
  }

  function renderAddress(place) {
    map.setCenter(place.geometry.location);
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
  }
}